"""Method to correct input and output schemas containing errors."""

from __future__ import annotations

from copy import deepcopy
from json import JSONDecodeError
from typing import TYPE_CHECKING

import orjson
from json_repair import repair_json

try:
    from rapidfuzz.distance import Indel
except ImportError:
    Indel = None

from .constants import (
    ERR_INPUT_SCHEMA_LEAF_TYPE_INVALID,
    ERR_LABEL_ARRAY_HAS_DUPLICATED_ELEMENTS,
    ERR_LABEL_ARRAY_ITEM_IS_NULL,
    ERR_LABEL_ARRAY_VALUE_IS_BASE_TYPE_INSTEAD_OF_ARRAY,
    ERR_LABEL_ARRAY_VALUE_IS_NULL_INSTEAD_OF_EMPTY_ARR,
    ERR_LABEL_ARRAY_VALUE_IS_NULL_INSTEAD_OF_EMPTY_DICT,
    ERR_LABEL_ENUM_VALUE_IS_A_LIST_INSTEAD_OF_BASE_TYPE,
    ERR_LABEL_ENUM_VALUE_NOT_IN_INPUT_SCHEMA,
    ERR_LABEL_LEAF_TYPE_INVALID,
    ERR_LABEL_LEAF_VALUE_IS_NOT_NULL_WHEREAS_INPUT_TEXT_IS,
    ERR_LABEL_MISSING_NODE_FROM_INPUT_SCHEMA,
    ERR_LABEL_MULTI_ENUM_IS_LIST_OF_LIST,
    ERR_LABEL_MULTI_ENUM_VALUE_NOT_IN_INPUT_SCHEMA,
    ERR_LABEL_NODE_NOT_IN_INPUT_SCHEMA,
    ERR_LABEL_NODE_VALUE_IS_ARRAY_INSTEAD_OF_DICT,
    ERR_LABEL_NODE_VALUE_IS_BASE_TYPE_INSTEAD_OF_DICT,
    ERR_LABEL_NODE_VALUE_IS_DICT_INSTEAD_OF_ARRAY,
    ERR_LABEL_NOT_JSON_DESERIALIZABLE,
    INDEL_THRESHOLD_INPUT_TYPE,
    INDEL_THRESHOLD_OUTPUT_ENUM,
    INDEL_THRESHOLD_OUTPUT_NODE_NAME,
)
from .data_validation import (
    detect_errors_in_input_template,
    detect_errors_in_output_json,
)
from .models import ErrorJson
from .types import NUEXTRACT_DEFAULT_TYPES
from .utils import group_identical_elements, mock_schema

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence


def _find_closest_value_indel(
    enum: Sequence[str], value: str, max_indel_distance: int
) -> tuple[int, int] | None:
    if Indel is None:
        return None

    indel_distances = [
        (idx, indel_dist)
        for idx, input_val in enumerate(enum)
        if isinstance(input_val, str)
        and (indel_dist := Indel.distance(input_val, value)) <= max_indel_distance
    ]
    if len(indel_distances) > 0:
        if len(indel_distances) > 1:
            dist_min = min(indel_distances, key=lambda x: x[1])[1]
            indel_distances = [
                (idx, dist) for idx, dist in indel_distances if dist == dist_min
            ]
        return indel_distances[0]
    return None


def correct_input_template(
    schema: dict | list | str,
    leaf_types: Mapping[str, type] = NUEXTRACT_DEFAULT_TYPES,
    indel_distance_input_type: int | None = INDEL_THRESHOLD_INPUT_TYPE,
) -> tuple[dict | list, list[ErrorJson]]:
    """
    Correct a schema by removing leaves with types that are absent from the predefined.

    All leaves with errors are deleted by default as correcting them programmatically
    cannot be done reliably.

    :param schema: input schema to correct.
    :param leaf_types: dictionary mapping leaf types names to the associated expected
        Python type (default: ``TYPE_NAME_TO_TYPE``).
    :param indel_distance_input_type: maximum indel (insertion-deletion) distance
        allowing to edit an invalid leaf type in the input schema to one from
        ``leaf_types``, if their indel distance does not exceed this threshold.
        (default: ``2``)
    :return: whether the labels follow the same structure as the schema.
    :raise JSONDecodeError: if the schema is provided as a string and cannot be parsed,
        and repaired.
    """
    # Store list of errors in hash list
    # `past_errors` stores of input errors.
    past_errors = set()
    errors_fixed_set = set()
    errors_fixed = []

    # First handle "non JSON-serializable" errors if any.
    # In some cases, the json.loads methods doesn't throw an exception but returns
    # a string, which can be parsed as a dictionary when provided to the json.loads
    # method again.
    if not isinstance(schema, (dict, list)):
        input_schema_copy = load_json_and_repair_if_required(schema)
    else:
        input_schema_copy = deepcopy(schema)

    # Correct input schema while there are errors and that the list of detected
    # errors hasn't been treated already (otherwise it'll loop).
    errors = detect_errors_in_input_template(input_schema_copy, leaf_types)
    errors_json = tuple(err.to_json() for err in errors)
    while len(errors) > 0 and errors_json not in past_errors:
        input_schema_copy = _correct_input_schema(
            input_schema_copy, errors, leaf_types, indel_distance_input_type
        )
        past_errors.add(errors_json)
        # New error detection
        errors_before = errors.copy()
        errors_json_before = errors_json
        errors = detect_errors_in_input_template(input_schema_copy, leaf_types)
        errors_json = tuple(err.to_json() for err in errors)
        # Recording errors fixed
        for err, err_json in zip(errors_before, errors_json_before):
            if err_json not in errors_fixed_set and err_json not in errors_json:
                errors_fixed.append(err)
                errors_fixed_set.add(err_json)

    return input_schema_copy, errors_fixed


def _correct_input_schema(
    schema: dict | list,
    errors: list[ErrorJson],
    leaf_types: Mapping[str, type] = NUEXTRACT_DEFAULT_TYPES,
    indel_distance_threshold: int | None = INDEL_THRESHOLD_INPUT_TYPE,
) -> dict | list:
    """
    Corrects a schema in-place based on a list of errors.

    This function iterates through a list of `ErrorJson` objects and attempts to fix
    the schema. It can correct misspelled leaf types or delete invalid nodes. When a
    leaf type is corrected, it updates the `value_fixed` attribute of the
    corresponding `ErrorJson` object.
    """
    # Special case where the schema is an empty dict/array, it might be flagged as an
    # error but there is nothing to correct
    if not schema:
        return schema

    # Backtracking method
    def helper(
        sub_schema: list | dict,
        error: ErrorJson,
        remaining_path: list[str | int],
    ) -> None:
        """
        Recursively traverses the schema to find and fix an error.

        :param sub_schema: The current branch of the schema being explored.
        :param error: The full ErrorJson object being processed. This allows
                      modifying it in the base case.
        :param remaining_path: The portion of the error path yet to be traversed.
        """
        current_key = remaining_path[0]

        # Recursive step: Go deeper into the schema until the parent of the leaf node.
        if len(remaining_path) > 1:
            # Ensure the path still exists before recursing
            if current_key in sub_schema:
                helper(sub_schema[current_key], error, remaining_path[1:])
            else:
                # The path has already been deleted by a previous correction, so we stop
                return

        # Base case: We are at the parent of the erroneous node. Handle the error.
        else:
            # Check for the specific error type to attempt a correction.
            if (
                error.error_message == ERR_INPUT_SCHEMA_LEAF_TYPE_INVALID
                and isinstance(sub_schema[current_key], str)
                and sub_schema[current_key] != ""
            ):
                erroneous_value = sub_schema[current_key]
                correction_made = False
                for leaf_type in leaf_types:
                    if (
                        Indel is not None
                        and indel_distance_threshold is not None
                        and Indel.distance(erroneous_value, leaf_type)
                        <= indel_distance_threshold
                    ):
                        # Apply the correction to the schema
                        sub_schema[current_key] = leaf_type
                        # **MODIFICATION: Update the error object with the fixed value**
                        error.value_fixed = leaf_type
                        correction_made = True
                        break

                # If no suitable correction was found, delete the invalid leaf.
                if not correction_made:
                    del sub_schema[current_key]

            # For any other error type, just delete the leaf.
            else:
                error.node_deleted = True
                del sub_schema[current_key]
            return

        # Backtracking step: After returning from recursion, check if the child node
        # we just explored has become empty (dict or list). If so, prune it.
        if current_key in sub_schema and not sub_schema[current_key]:
            del sub_schema[current_key]

    # Create a deep copy to avoid modifying the original schema
    schema_copy = deepcopy(schema)
    for error_ in errors:
        # We only process errors that have a path to follow
        if error_.path:
            helper(schema_copy, error_, error_.path)

    return schema_copy


def _correct_output_schema(
    schema: dict | list,
    labels: dict | list,
    errors: list[ErrorJson],
    leaf_types: Mapping[str, type] = NUEXTRACT_DEFAULT_TYPES,
    indel_distance_enum_value: int | None = INDEL_THRESHOLD_OUTPUT_ENUM,
    indel_distance_node_name: int | None = INDEL_THRESHOLD_OUTPUT_NODE_NAME,
    delete_unfixable_nodes_from_input: bool = False,
    deduplicate_arrays_entries: bool = False,
    input_text: str | list[str] | None = None,
) -> tuple[dict | list, dict | list]:
    """
    Correct labels according to the input schema and flagged errors.

    The method will traverse the output tree and try to fix problematic leaf values.

    The input ``schema`` is expected to be error-free and 100% valid.
    The method uses backtracking to first correct the leaves, then deleting at each
    depth the empty child nodes.

    Here follow the errors and their resolutions (or not if "/"):
    "label date-time value not ISO 8601 compliant": /
    "label classification value is a list instead of base type": unsqueeze list value if
        its length is 1, else delete node
    "label leaf value type is not valid": conversion between str - int/float/bool/dt
    "label country name value is not ISO 3166 compliant": /
    "label array has duplicated element(s)": deduplicate
    "label multi-classification value(s) not in input schema": remove non-existent items
    "label classification value not in input schema": delete node
    "label node value is a dictionary instead of an array": delete node
    "label currency code value is not ISO 4217 compliant": /
    "label array value is null instead of empty []": convert to []
    "label array value is base type instead of an array": put value in an array
    "label node value is base type instead of a dict": delete node

    :param schema: schema to follow as a dictionary.
    :param labels: labels to correct.
    :param errors: list of errors present in the labels schema, provided as a list of
        tuples holding the paths in the schema tree to the error (as a list of nodes
        names) and the error message.
    :param leaf_types: dictionary mapping leaf types names to the associated expected
        Python type (default: ``TYPE_NAME_TO_TYPE``).
    :param indel_distance_enum_value: maximum indel (insertion-deletion) distance
        allowing to fix the value of an invalid enum with one from the expected values
        provided in the input schema, if their indel distance does not exceed this
        threshold. (default: ``None``)
    :param indel_distance_node_name: maximum indel (insertion-deletion) distance
        allowing to change the name of a node in the output schema which is not present
        in the input schema with the name of a node in the input schema which is missing
        from the output schema, at the same level (i.e. with the same parent node). This
        is typically useful when a model generated a "typo" in the node name.
        (default: ``None``)
    :param delete_unfixable_nodes_from_input: if provided as ``True``, the method may
        delete nodes from the input and output schemas instead of setting leaf values to
        ``null``/empty entries. This argument allows the input schema to be modified.
         Providing it to ``True`` might allow to change ``verbatim-string`` leaf types
         to ``string``. (default: ``False``)
    :param deduplicate_arrays_entries: deduplicate entries in arrays, primitives and
        objects. (default: ``False``)
    :param input_text: text input to extract the information from the schema from.
    :return: the updated input and output schemas.
    """
    # Special case where the schema is an empty dict/array, it might be flagged as an
    # error but there is nothing to correct
    if len(schema) == 0:
        return ({}, {}) if isinstance(schema, dict) else ([], [])
    # Special case where the root is an array instead of dict and vice-versa
    if (
        len(errors) > 0
        and len(errors[0].path) == 0
        and errors[0].error_message
        in (
            ERR_LABEL_NODE_VALUE_IS_ARRAY_INSTEAD_OF_DICT,
            ERR_LABEL_NODE_VALUE_IS_DICT_INSTEAD_OF_ARRAY,
        )
    ):
        if not delete_unfixable_nodes_from_input:
            return schema, mock_schema(schema)
        # Deleting unfixable nodes, so just returning empty schema and output
        if isinstance(schema, dict):
            return {}, {}
        return [], []

    current_error_idx = 0
    current_path = []

    # Remove duplicated array element if not fixing these errors
    if not deduplicate_arrays_entries:
        for idx_ in reversed(range(len(errors))):
            if errors[idx_].error_message == ERR_LABEL_ARRAY_HAS_DUPLICATED_ELEMENTS:
                del errors[idx_]

    # Correct the schema for each error
    # Order the errors per idx in decreasing order
    errors = _sort_errors_json(errors)

    def delete_errors_pointing_to_deleted_node(
        path_to_delete: Sequence[str | int],
    ) -> None:
        # Delete the errors that point to leaves inside of it.
        if current_error_idx == len(errors) - 1:
            return
        for idx_err_to_process in reversed(range(current_error_idx + 1, len(errors))):
            err_to_process_path = errors[idx_err_to_process].path
            if err_to_process_path[: len(path_to_delete)] == path_to_delete:
                del errors[idx_err_to_process]

    def get_errors_at_same_level_of_current_one_indel(
        output_node_name: str, err_msg: str
    ) -> tuple[str, int] | None:
        # Return errors with the same parent node as the current one, with an error
        # message equal to `err_msg` and a final node name with an indel distance with
        # `output_node_name` lower or equal to indel_distance_node_name.
        # --> get node names that can replace `output_node_name` (which is missing
        # from either the input or output schema)
        if Indel is None:
            return None

        errors_at_same_location = [
            (idx, error)
            for idx, error in enumerate(errors)
            if error.path[:-1] == current_path
            and error.error_message == err_msg
            and not error.node_deleted
        ]
        if len(errors_at_same_location) == 0:
            return None

        indel_distances = [
            (idx, indel_dist)
            for idx, error in errors_at_same_location
            if (indel_dist := Indel.distance(str(error.path[-1]), output_node_name))
            <= indel_distance_node_name
        ]
        if len(indel_distances) > 0:
            if len(indel_distances) > 1:
                dist_min = min(indel_distances, key=lambda x: x[1])[1]
                indel_distances = [
                    (idx, dist) for idx, dist in indel_distances if dist == dist_min
                ]
                if len(indel_distances) > 1:
                    return None
            return errors[indel_distances[0][0]].path[-1], indel_distances[0][0]
        return None

    # Backtracking method
    def helper(
        schema_: list | dict,
        labels_: list | dict,
        error: ErrorJson,
        remaining_path: list[str | int],
    ) -> None:
        # Check that the element the error step is pointing to is present in the schema.
        # It could have been deleted with backtracking when processing a previous error,
        # especially if the current error is "label missing node from the input schema".
        if (
            current_error_idx > 0
            and error.error_message == ERR_LABEL_MISSING_NODE_FROM_INPUT_SCHEMA
            and (
                len(schema_) == 0
                if isinstance(schema_, list)
                else remaining_path[0] not in schema_
            )
        ):
            # would be better to check if a previous error pointed to the current step
            # in the tree, to double-check that the node has been deleted previously and
            # this is not a bug
            return
        # First go to the last node before the leaf to treat
        # Create a copy of the child branch, as it might be modified inplace, whereas
        # the original might be needed if the current node is an array.
        schema_child_copy = None
        if len(remaining_path) > 1:
            schema_child_copy = deepcopy(
                schema_[0 if isinstance(schema_, list) else remaining_path[0]]
            )
            current_path.append(remaining_path[0])
            # MODIFICATION: Pass error object and remaining path in recursive call
            helper(
                schema_[0 if isinstance(schema_, list) else remaining_path[0]],
                labels_[remaining_path[0]],
                error,
                remaining_path[1:],
            )
            current_path.pop(-1)

        # Process problematic leaf
        # Note: after correction, the leaf value might still be invalid (e.g. array
        # (un)squeeze.
        if len(remaining_path) == 1:
            leaf_key = remaining_path[0]
            schema_is_array = (
                isinstance(schema_, list)
                and isinstance(leaf_key, int)
                and len(schema_) == 1
            )
            error_msg = error.error_message

            # Non-null value whereas it should have been
            # For each correction, error.value_fixed is updated
            if error_msg == ERR_LABEL_LEAF_VALUE_IS_NOT_NULL_WHEREAS_INPUT_TEXT_IS:
                labels_[leaf_key] = None
                error.value_fixed = None
            # Enum returned as array
            elif error_msg == ERR_LABEL_ENUM_VALUE_IS_A_LIST_INSTEAD_OF_BASE_TYPE:
                if len(labels_[leaf_key]) == 1:
                    fixed_value = labels_[leaf_key][0]
                    labels_[leaf_key] = fixed_value
                    error.value_fixed = fixed_value
                else:
                    if delete_unfixable_nodes_from_input:
                        del schema_[leaf_key]
                        del labels_[leaf_key]
                        error.node_deleted = True
                    else:
                        # Set leaf value to None by default, then take the first item
                        # from the labels that is also in the schema
                        enum_value = None
                        for item in labels_[leaf_key]:
                            if item in schema_[leaf_key]:
                                enum_value = item
                                break
                        labels_[leaf_key] = enum_value
                        error.value_fixed = enum_value
            # Enum value not in input schema
            elif error_msg == ERR_LABEL_ENUM_VALUE_NOT_IN_INPUT_SCHEMA:
                # If indel distance threshold provided, see if a value from the input
                # can be used to replace the one in the output schema
                replaced = False  # var used to handle next if conditions
                if indel_distance_enum_value and isinstance(
                    labels_[leaf_key], (str, int, float)
                ):
                    value = (
                        labels_[leaf_key]
                        if isinstance(labels_[leaf_key], str)
                        else str(labels_[leaf_key])
                    )
                    indel_res = _find_closest_value_indel(
                        schema_[leaf_key], value, indel_distance_enum_value
                    )
                    if indel_res is not None:
                        fixed_value = schema_[leaf_key][indel_res[0]]
                        labels_[leaf_key] = fixed_value
                        error.value_fixed = fixed_value
                        replaced = True

                if not replaced:
                    if delete_unfixable_nodes_from_input:
                        del schema_[leaf_key]
                        del labels_[leaf_key]
                        error.node_deleted = True
                    else:
                        labels_[leaf_key] = None
                        error.value_fixed = None
            # Array value is base type instead of array
            elif error_msg == ERR_LABEL_ARRAY_VALUE_IS_BASE_TYPE_INSTEAD_OF_ARRAY:
                fixed_value = [labels_[leaf_key]]
                labels_[leaf_key] = fixed_value
                error.value_fixed = fixed_value
            elif error_msg == ERR_LABEL_ARRAY_ITEM_IS_NULL:
                del labels_[leaf_key]
            # Array with duplicates
            # Check that the leaf_key is in labels_ because the list might have been
            # deleted when processing previous errors, if all items were erroneous and
            # have been deleted (thus the whole node too when backtracking the dict).
            elif (
                error_msg == ERR_LABEL_ARRAY_HAS_DUPLICATED_ELEMENTS
                and leaf_key in labels_
            ):
                # Identify idx that are duplicates (tuples of n identical items)
                # Storing the deduplicated array in error.
                original_len = len(labels_[leaf_key])
                groups_duplicated_items = group_identical_elements(labels_[leaf_key])

                # List the indexes of the items to delete. Select all items within each
                # group except the lowest idx.
                idxs_to_delete = [
                    idx for idxs, _ in groups_duplicated_items for idx in idxs[1:]
                ]

                # Delete the items and update the idx of the errors not processed yet
                # mapping to elements within the array.
                for idx_to_del in sorted(idxs_to_delete, reverse=True):
                    # First decrement indexes of errors pointing to items within the
                    # array to array currently being deduplicated, that are greater than
                    # the idx of the item to delete (idx_to_del)
                    path_to_arr = [*current_path, leaf_key]
                    for idx_err_to_process in reversed(
                        range(current_error_idx + 1, len(errors))
                    ):
                        err_to_process_path = errors[idx_err_to_process].path
                        # Only cover errors pointing to items in array and deeper
                        if len(err_to_process_path) > len(path_to_arr):
                            # +1 to include the index/path step of the child item
                            err_to_process_path = err_to_process_path[
                                : len(path_to_arr) + 1
                            ]
                            if (
                                err_to_process_path[: len(path_to_arr)] == path_to_arr
                                and err_to_process_path[-1] > idx_to_del
                            ):
                                errors[idx_err_to_process].path[len(path_to_arr)] -= 1

                    delete_errors_pointing_to_deleted_node([*path_to_arr, idx_to_del])
                    # Delete the item from the array
                    del labels_[leaf_key][idx_to_del]

                if len(labels_[leaf_key]) != original_len:
                    error.value_fixed = labels_[leaf_key]
            # Multi-enum is list of list (e.g. [[0, 1]] instead of [0, 1])
            elif error_msg == ERR_LABEL_MULTI_ENUM_IS_LIST_OF_LIST:
                fixed_value = labels_[leaf_key][0]
                labels_[leaf_key] = fixed_value
                error.value_fixed = fixed_value
            # Multi-enum value(s) not in input schema
            elif error_msg == ERR_LABEL_MULTI_ENUM_VALUE_NOT_IN_INPUT_SCHEMA:
                replaced = False
                if indel_distance_enum_value and isinstance(
                    labels_[leaf_key], (str, int, float)
                ):
                    value = (
                        labels_[leaf_key]
                        if isinstance(labels_[leaf_key], str)
                        else str(labels_[leaf_key])
                    )
                    indel_res = _find_closest_value_indel(
                        schema_[0], value, indel_distance_enum_value
                    )
                    if indel_res is not None:
                        fixed_value = schema_[0][indel_res[0]]
                        labels_[leaf_key] = fixed_value
                        error.value_fixed = fixed_value
                        replaced = True
                if not replaced:
                    del labels_[leaf_key]
                    error.node_deleted = True
            # Node value is null instead of dictionary/branch
            elif error_msg == ERR_LABEL_ARRAY_VALUE_IS_NULL_INSTEAD_OF_EMPTY_DICT:
                fixed_value = mock_schema(schema_[leaf_key])
                labels_[leaf_key] = fixed_value
                error.value_fixed = orjson.dumps(fixed_value).decode()
            # Array value is null instead of empty []
            elif error_msg == ERR_LABEL_ARRAY_VALUE_IS_NULL_INSTEAD_OF_EMPTY_ARR:
                labels_[leaf_key] = []
                error.value_fixed = []
            # array/dict instead of the dict/array
            elif error_msg in {
                ERR_LABEL_NODE_VALUE_IS_BASE_TYPE_INSTEAD_OF_DICT,
                ERR_LABEL_NODE_VALUE_IS_ARRAY_INSTEAD_OF_DICT,
            }:
                # Unsqueeze array to dict mapping to an array
                if (
                    error_msg == ERR_LABEL_NODE_VALUE_IS_ARRAY_INSTEAD_OF_DICT
                    and len(schema_[leaf_key if isinstance(schema_, dict) else 0]) == 1
                    and isinstance(next(iter(schema_[leaf_key].values())), list)
                    and isinstance(next(iter(schema_[leaf_key].values()))[0], dict)
                ):
                    labels_[leaf_key] = {
                        next(iter(schema_[leaf_key].keys())): labels_[leaf_key]
                    }
                # Mock node
                elif not delete_unfixable_nodes_from_input:
                    fixed_value = mock_schema(
                        schema_[0 if schema_is_array else leaf_key]
                    )
                    labels_[leaf_key] = fixed_value
                    error.value_fixed = fixed_value
                # Delete node from input/output
                else:
                    if not isinstance(leaf_key, int):
                        del schema_[leaf_key]
                    del labels_[leaf_key]
                    error.node_deleted = True
            elif (
                error_msg == ERR_LABEL_NODE_VALUE_IS_DICT_INSTEAD_OF_ARRAY
                and not delete_unfixable_nodes_from_input
            ):
                labels_[leaf_key] = []
                error.value_fixed = []
            # FP/FN nodes
            # If fixing these errors by renaming the node name (as can be the result of
            # a "typo"), make sure that the "node in output missing from input" error is
            # treated first, so that the node "in input but missing from output" isn't
            # added/mocked first.
            elif error_msg == ERR_LABEL_MISSING_NODE_FROM_INPUT_SCHEMA:
                fixed = False
                # First try to fix it by checking if it is close enough to a node name
                # already present in the outputs
                if indel_distance_node_name:
                    result = get_errors_at_same_level_of_current_one_indel(
                        leaf_key, ERR_LABEL_NODE_NOT_IN_INPUT_SCHEMA
                    )
                    if result is not None:
                        # leaf_key is not present in the labels
                        value_fixed = labels_[result[0]]
                        labels_[leaf_key] = value_fixed
                        error.value_fixed = value_fixed
                        del labels_[result[0]]
                        del errors[result[1]]  # delete error of node missing in output
                        fixed = True

                if fixed:
                    pass
                elif delete_unfixable_nodes_from_input:
                    del schema_[leaf_key]
                    error.node_deleted = True
                else:
                    if isinstance(schema_[leaf_key], dict):
                        value_fixed = mock_schema(schema_[leaf_key])
                        labels_[leaf_key] = value_fixed
                        error.value_fixed = orjson.dumps(value_fixed).decode()
                    elif (
                        isinstance(schema_[leaf_key], list)
                        and len(schema_[leaf_key]) <= 1
                    ):
                        labels_[leaf_key] = []
                        error.value_fixed = []
                    else:
                        labels_[leaf_key] = None
            elif error_msg == ERR_LABEL_NODE_NOT_IN_INPUT_SCHEMA:
                fixed = False
                if indel_distance_node_name:
                    result = get_errors_at_same_level_of_current_one_indel(
                        leaf_key, ERR_LABEL_MISSING_NODE_FROM_INPUT_SCHEMA
                    )
                    if result is not None:
                        value_fixed = labels_[leaf_key]
                        labels_[result[0]] = value_fixed
                        error.value_fixed = value_fixed
                        del labels_[leaf_key]
                        del errors[result[1]]  # delete error of node missing in input
                        fixed = True

                if fixed:
                    pass
                else:
                    del labels_[leaf_key]
                    error.node_deleted = True
            # Handle case where the prediction is an array instead of base type, by
            # squeezing what's inside hoping it's a valid value
            elif error_msg == ERR_LABEL_LEAF_TYPE_INVALID and isinstance(
                labels_[leaf_key], list
            ):
                # If the list is non-empty, pick the first squeeze the first item
                if len(labels_[leaf_key]) > 0:
                    fixed_value = labels_[leaf_key][0]
                    labels_[leaf_key] = fixed_value
                    error.value_fixed = fixed_value
                else:  # otherwise set the leaf it to null
                    labels_[leaf_key] = None
                    error.value_fixed = None
            # Type validation error: try to fix it by calling the type
            # It also includes ERR_LABEL_LEAF_TYPE_INVALID not covered yet (special
            # cases above)
            else:
                leaf_type = schema_[0 if schema_is_array else leaf_key]
                try:
                    # Invalid boolean-like values cannot be coerced safely: Python's
                    # bool would map every non-empty string, including "no", to True.
                    if leaf_types[leaf_type] is bool:
                        value_fixed = None
                    else:
                        value_fixed = leaf_types[leaf_type](
                            labels_[leaf_key], input_text, error
                        )

                    # Set node deletion if not set by type class
                    if error.node_deleted is None:
                        error.node_deleted = (
                            value_fixed is None and delete_unfixable_nodes_from_input
                        )
                    # Delete node or apply fixed value
                    if error.node_deleted:
                        # Do not edit the input schema if is an array
                        if not isinstance(leaf_key, int):
                            del schema_[leaf_key]
                        del labels_[leaf_key]
                    else:
                        # Apply fixed value
                        labels_[leaf_key] = value_fixed
                        error.value_fixed = value_fixed
                except ValueError:
                    # Remove invalid item if current depth is an array
                    if schema_is_array or delete_unfixable_nodes_from_input:
                        if (
                            not isinstance(leaf_key, int)
                            and delete_unfixable_nodes_from_input
                        ):
                            del schema_[leaf_key]
                        del labels_[leaf_key]
                        error.node_deleted = True
                    else:
                        labels_[leaf_key] = None
            return

        # Current node/depth is a list
        # Check that the item processed still comply to the schema, otherwise delete it.
        # The element can however contain errors that are referenced in the errors to
        # fix.
        if isinstance(schema_, list):
            # Set back the schema branch to its original as it may have been altered.
            # It's only possible to alter the input schema here if there is one element
            # in the array, otherwise it would probably make the other items not
            # compliant.
            if len(labels_) > 1:
                schema_[0] = schema_child_copy
            else:  # update the schema (already done inplace)
                return  # we can just return as the array item is schema-compliant then

            # The following code checks that the branch starting from the item in the
            # list follows the schema. It checks that the node of the leaf to correct is
            # still present, otherwise it has probably been deleted (might not if the
            # error is to ignore).
            # If the leaf to which the error points is an item in an array (base-type
            # array or multi-enum), the node will still be there so there is no need to
            # check. (+ path part is an integer index, can't check presence in list)
            if isinstance(remaining_path[-1], int):
                return
            try:
                node_before_leaf_to_correct = _traverse_tree(
                    labels_, remaining_path[:-1], valid_func=None
                )
            # IndexError will happen if an item in an array downstream has been deleted
            # KeyError will happen if an empty dict has been deleted downstream.
            except (IndexError, KeyError):  # In this case we can just return
                return
            if remaining_path[-1] in node_before_leaf_to_correct or (
                remaining_path[-1] not in node_before_leaf_to_correct
                and error.error_message == ERR_LABEL_NODE_NOT_IN_INPUT_SCHEMA
            ):
                return  # leaf has been corrected, nothing more to do
            del labels_[remaining_path[0]]  # delete the array item

            # Delete the errors that point to leaves inside of it.
            delete_errors_pointing_to_deleted_node([*current_path, remaining_path[0]])
            return

        # Dict
        # Check that the child branch just explored is not empty.
        if delete_unfixable_nodes_from_input and len(labels_[remaining_path[0]]) == 0:
            del labels_[remaining_path[0]]
            del schema_[remaining_path[0]]
            delete_errors_pointing_to_deleted_node([*current_path, remaining_path[0]])

    input_schema_copy, labels_schema_copy = deepcopy(schema), deepcopy(labels)

    # Root arrays have no path component for the generic tree traversal below.
    if deduplicate_arrays_entries and isinstance(labels_schema_copy, list):
        for error_index in reversed(range(len(errors))):
            error = errors[error_index]
            if (
                not error.path
                and error.error_message == ERR_LABEL_ARRAY_HAS_DUPLICATED_ELEMENTS
            ):
                duplicate_indices = [
                    item_index
                    for item_indices, _ in group_identical_elements(labels_schema_copy)
                    for item_index in item_indices[1:]
                ]
                for duplicate_index in sorted(duplicate_indices, reverse=True):
                    del labels_schema_copy[duplicate_index]
                error.value_fixed = labels_schema_copy
                del errors[error_index]

    while current_error_idx < len(errors):  # errors might get deleted inplace in helper
        current_error = errors[current_error_idx]
        helper(
            input_schema_copy,
            labels_schema_copy,
            current_error,
            current_error.path.copy(),
        )
        current_error_idx += 1
    return input_schema_copy, labels_schema_copy


def _sort_errors_json(error_list: list[ErrorJson]) -> list[ErrorJson]:
    """
    Sort a list of ErrorJson objects based on their path attribute.

    The sorting is done by the path's string prefix first, and then by any
    integer indices in descending order. This ensures that when multiple paths
    explore the same array, the errors for items with the highest indexes
    appear first.

    :param error_list: A list of ErrorJson objects.
    :return: A new list of ErrorJson objects, sorted.
    """

    def create_sorting_key(
        error_obj: ErrorJson,
    ) -> tuple[tuple[str, ...], tuple[int, ...]]:
        """Create a composite key from the ErrorJson's path."""
        path = error_obj.path

        # Collect the initial sequence of strings for grouping
        string_prefix = []
        for item in path:
            if isinstance(item, str):
                string_prefix.append(item)
            else:
                # Stop at the first non-string item (e.g., an integer index)
                break

        # Collect all integers from the path, negating them for descending sort order
        int_values = [-item for item in path if isinstance(item, int)]

        # The key is a tuple: first sort by the string part, then by the numbers
        return tuple(string_prefix), tuple(int_values)

    return sorted(error_list, key=create_sorting_key)


def _traverse_tree(
    tree: dict,
    path: Sequence[str | int],
    valid_func: Callable[[dict, Sequence[str | int]], bool] | None,
) -> object:
    """
    Traverse a tree dictionary through the specified ``path`` and return its end node.

    This method assumes that all the steps in the specified ``path`` are present in the
    ``tree``.

    :param tree: tree to traverse.
    :param path: path to take as a list of dictionary keys or list indexes.
    :param valid_func: a method stopping the tree traverse. It takes the current
        ``tree`` branch and the current ``path`` as arguments and returns a ``bool``.
        (default: ``None``)
    :return: node at the end of the ``path``.
    """
    return (
        tree
        if len(path) == 0 or (valid_func is not None and not valid_func(tree, path))
        else _traverse_tree(tree[path[0]], path[1:], valid_func)
    )


def load_json_and_repair_if_required(json_string: str) -> dict | list:
    """
    Load a JSON string with ``orjson`` and repair if it is malformed.

    :param json_string: JSON string to load.
    :return: the JSON string as objects, if it can be loaded or repaired, otherwise
        ``None``.
    """
    try:
        data = orjson.loads(json_string)
    except JSONDecodeError:
        # Skipping redundant JSON load as we already know that the JSON is malformed
        data = repair_json(
            json_string,
            skip_json_loads=True,
            ensure_ascii=False,
            stream_stable=True,
            return_objects=True,
        )
        if data is None or data == "":
            raise
    return data


def correct_output_json_and_input_template(
    schema_input: dict | list | str,
    schema_output: dict | list | str,
    input_text: str | list[str] | None,
    leaf_types: Mapping[str, type] = NUEXTRACT_DEFAULT_TYPES,
    indel_distance_input_type: int | None = INDEL_THRESHOLD_INPUT_TYPE,
    indel_distance_output_enum: int | None = INDEL_THRESHOLD_OUTPUT_ENUM,
    indel_distance_node_name: int | None = INDEL_THRESHOLD_OUTPUT_NODE_NAME,
    delete_unfixable_nodes_from_output: bool = False,
    deduplicate_arrays_entries: bool = False,
    return_empty_output_schema_if_too_much_malformed: bool = True,
) -> tuple[dict | list, dict | list | str, list[ErrorJson], list[ErrorJson]]:
    """
    Correct a pair of input and output schemas iteratively.

    After running the ``correct_output_schema`` method, some label leaf values might
    still be invalid according to the input schema, for example if unsqueezing an array
    value which is of an invalid type such as string instead of float.
    This method iteratively calls ``correct_output_schema`` until the labels schema
    is completely corrected or cannot be further.

    If one of the schemas cannot be parsed (i.e. is not JSON-serializable), the method
    returns them as they are provided.

    :param schema_input: input schema.
    :param schema_output: labels schema.
    :param input_text: text input to extract the information from the schema from.
    :param leaf_types: dictionary mapping leaf types names to the associated expected
        Python type (default: ``TYPE_NAME_TO_TYPE``).
    :param indel_distance_input_type: maximum indel (insertion-deletion) distance
        allowing to edit an invalid leaf type in the input schema to one from
        ``leaf_types``, if their indel distance does not exceed this threshold.
        (default: ``2``)
    :param indel_distance_output_enum: maximum indel (insertion-deletion) distance
        allowing to edit an invalid leaf type in the input schema to one from
        ``leaf_types``, if their indel distance does not exceed this threshold.
        (default: ``2``)
    :param indel_distance_node_name: maximum indel (insertion-deletion) distance
        allowing to change the name of a node in the output schema which is not present
        in the input schema with the name of a node in the input schema which is missing
        from the output schema, at the same level (i.e. with the same parent node). This
        is typically useful when a model generated a "typo" in the node name.
        (default: ``2``)
    :param delete_unfixable_nodes_from_output: if provided as ``True``, the method may
        delete nodes from the input and output schemas instead of setting leaf values to
        ``null``/empty entries. This argument allows the input schema to be modified.
         Providing it to ``True`` might allow to change ``verbatim-string`` leaf types
         to ``string``. (default: ``False``)
    :param deduplicate_arrays_entries: deduplicate entries in arrays, primitives and
        objects. (default: ``False``)
    :param return_empty_output_schema_if_too_much_malformed: whether to return an empty
        ``schema_output`` (following the ``schema_input`` structure) if provided as a
        string and being to much malformed that it cannot be fixed. If this argument is
        provided as ``False``, the original ``schema_output`` string is returned in the
        output tuple. (default: ``True``)
    :return: input and labels schemas fixed as much as the method can.
    :raise JSONDecodeError: if the input schema is provided as a string and cannot be
        parsed and repaired, or output if
        ``return_empty_output_schema_if_too_much_malformed`` is ``False``.
    """
    # First handle "non JSON-serializable" errors if any.
    # In some cases, the json.loads methods doesn't throw an exception but returns
    # a string, which can be parsed as a dictionary when provided to the json.loads
    # method again.
    if not isinstance(schema_input, (dict, list)):
        input_schema_copy = load_json_and_repair_if_required(schema_input)
    else:
        input_schema_copy = deepcopy(schema_input)
    if not isinstance(schema_output, (dict, list)):
        try:
            labels_schema_copy = load_json_and_repair_if_required(schema_output)
        except JSONDecodeError:
            # Output JSON too much malformed that it can't be fixed
            if return_empty_output_schema_if_too_much_malformed:
                return (
                    input_schema_copy,
                    mock_schema(schema_input),
                    [],
                    [ErrorJson([], ERR_LABEL_NOT_JSON_DESERIALIZABLE)],
                )
            raise
    else:
        labels_schema_copy = deepcopy(schema_output)

    # First make sure there is no error in the input, correct it otherwise
    input_schema_copy, errors_fixed_input = correct_input_template(
        input_schema_copy, leaf_types, indel_distance_input_type
    )

    # Correct output while there are errors and that the list of detected
    # errors hasn't been treated already (otherwise it'll loop).
    past_errors = set()  # store output errors in a hash list.
    errors_fixed_set = set()
    errors_fixed = []
    errors = detect_errors_in_output_json(
        input_schema_copy, labels_schema_copy, input_text, leaf_types
    )
    errors_json = tuple(err.to_json() for err in errors)
    while len(errors) > 0 and errors_json not in past_errors:
        input_schema_copy, labels_schema_copy = _correct_output_schema(
            input_schema_copy,
            labels_schema_copy,
            errors,
            leaf_types,
            indel_distance_output_enum,
            indel_distance_node_name,
            delete_unfixable_nodes_from_output,
            deduplicate_arrays_entries,
            input_text,
        )
        past_errors.add(errors_json)
        # New error detection
        errors_before = errors.copy()
        errors_json_before = errors_json
        errors = detect_errors_in_output_json(
            input_schema_copy,
            labels_schema_copy,
            input_text,
            leaf_types,
        )
        errors_json = tuple(err.to_json() for err in errors)
        # Recording errors fixed
        for err, err_json in zip(errors_before, errors_json_before):
            if err_json not in errors_fixed_set and err_json not in errors_json:
                errors_fixed.append(err)
                errors_fixed_set.add(err_json)

    return input_schema_copy, labels_schema_copy, errors_fixed_input, errors_fixed
