"""Methods for input/output schemas validation and compliance."""

from __future__ import annotations

from copy import deepcopy
from json import JSONDecodeError
from typing import TYPE_CHECKING

import orjson

from .constants import (
    ERR_INPUT_SCHEMA_ARRAY_IS_EMPTY,
    ERR_INPUT_SCHEMA_DICT_EMPTY,
    ERR_INPUT_SCHEMA_ENUM_INVALID_TYPE,
    ERR_INPUT_SCHEMA_LEAF_TYPE_INVALID,
    ERR_INPUT_SCHEMA_NOT_JSON_DESERIALIZABLE,
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
)
from .models import ErrorJson
from .types import NUEXTRACT_DEFAULT_TYPES
from .types.base import SemanticType
from .utils import is_object_enum, is_object_multi_enum, mock_schema

if TYPE_CHECKING:
    from collections.abc import Mapping


def _valid_leaf_type(c1: object, c2: type) -> bool:
    """
    Check if a leaf value is of the expected type.

    This method handles the bool-int subclassing (allows to differentiate them) and
    the expected type to be a class subclassing the type of the leaf. This second case
    allows to use custom classes with user code handling the conversion of the leaf
    value, potentially covering special cases when correcting a schema.

    Examples:
    ```
    # False
    t1 = _valid_leaf_type(int(), float)
    t2 = _valid_leaf_type(float(), int)
    t3 = _valid_leaf_type(bool(), int)
    t4 = _valid_leaf_type(int(), bool)
    # True
    t5 = _valid_leaf_type(float(), float)
    t6 = _valid_leaf_type("", str)
    t7 = _valid_leaf_type(float(), Number)
    t8 = _valid_leaf_type(int(), Number)
    ```

    :param c1: leaf value to analyze.
    :param c2: expected type (or class).
    :return: whether the leaf value is of the expected type.

    """
    if isinstance(c2, type) and issubclass(c2, SemanticType):
        return c2.is_valid_primitive_instance(c1)

    # If type is identical, return True
    if type(c1) is c2:
        return True
    # Special case for int/bool, have to use type is
    if c2 is int or c2 is bool:
        return type(c1) is c2
    # expected class subclasses type of the var
    return issubclass(type(c1), c2)


def _base_case_validation(
    leaf_type_name: str,
    prediction: object,
    leaf_types: Mapping[str, type],
    text_input: str | list[str] | None,
) -> str | None:
    # Base cases can be None
    if prediction is None:
        return None

    # If the input is text and the text is empty, the prediction should have been
    # ``null``.
    if text_input is not None and (
        (isinstance(text_input, str) and text_input.strip() == "")
        or all(text.strip() == "" for text in text_input)
    ):
        return ERR_LABEL_LEAF_VALUE_IS_NOT_NULL_WHEREAS_INPUT_TEXT_IS

    # Expected input type is not among the existing types
    # Its an input schema error which is expected to be caught in the input errors
    # detection method. Returning None here
    if leaf_type_name not in leaf_types:
        return None

    # Check output is of the expected leaf type
    if not _valid_leaf_type(prediction, leaf_types[leaf_type_name]):
        return ERR_LABEL_LEAF_TYPE_INVALID

    # If the type has a `validate` method, call it while providing the prediction and
    # return an error message if it is not valid.
    if callable(getattr(leaf_types[leaf_type_name], "validate", None)):
        return leaf_types[leaf_type_name].validate(prediction, text_input)

    # Otherwise the value is considered valid.
    return None


def detect_errors_in_input_template(
    schema_input: dict | list | str,
    leaf_types: Mapping[str, type] = NUEXTRACT_DEFAULT_TYPES,
) -> list[ErrorJson]:
    """
    Recursively detects the errors in an input schema.

    :param schema_input: input schema to follow.
    :param leaf_types: dictionary mapping leaf types names to the associated expected
        Python type (default: ``TYPE_NAME_TO_TYPE``).
    :return: the errors in the input schema, as a lists of tuples containing the paths
        to the error in the schema and the error message.
    """
    schema_errors = []  # [((node_name), error_msg)]

    # Filter out non JSON-serializable samples
    if isinstance(schema_input, str) and schema_input in leaf_types:
        return []
    if isinstance(schema_input, str):
        try:
            schema_input = orjson.loads(schema_input)
        except JSONDecodeError:
            pass
        finally:
            if not isinstance(schema_input, (dict, list)):
                schema_errors.append(
                    ErrorJson([], ERR_INPUT_SCHEMA_NOT_JSON_DESERIALIZABLE)
                )
    if len(schema_errors) > 0:
        return schema_errors

    def helper(ref, current_tree_path: list[str]) -> None:  # noqa: ANN001
        # Base case
        if not isinstance(ref, (dict, list)):
            if ref not in leaf_types:
                schema_errors.append(
                    ErrorJson(
                        current_tree_path,
                        ERR_INPUT_SCHEMA_LEAF_TYPE_INVALID,
                        value_erroneous=ref,
                    )
                )

        # Array: enum, multi-enum or array
        elif isinstance(ref, list):
            # Empty ref array
            if len(ref) == 0:
                schema_errors.append(
                    ErrorJson(
                        current_tree_path,
                        ERR_INPUT_SCHEMA_ARRAY_IS_EMPTY,
                        value_erroneous=ref,
                    )
                )
                return
            # Recursive call for inner dict
            if len(ref) == 1 and isinstance(ref[0], dict):
                helper(ref[0], [*current_tree_path, 0])
                return
            # Multi-enum
            if is_object_multi_enum(ref):
                for idx, item in enumerate(ref[0]):
                    if not isinstance(item, str):
                        schema_errors.append(
                            ErrorJson(
                                [*current_tree_path, 0, idx],
                                ERR_INPUT_SCHEMA_ENUM_INVALID_TYPE,
                                value_erroneous=item,
                            )
                        )
                return
            # Array of an unknown type
            if len(ref) == 1 and (
                not isinstance(ref[0], str) or ref[0] not in leaf_types
            ):
                schema_errors.append(
                    ErrorJson(
                        [*current_tree_path, 0],
                        ERR_INPUT_SCHEMA_LEAF_TYPE_INVALID,
                        value_erroneous=ref[0],
                    )
                )
                return
            # Enum: make sure all contain strings only
            if is_object_enum(ref):
                for idx, item in enumerate(ref):
                    if not isinstance(item, str):
                        schema_errors.append(
                            ErrorJson(
                                [*current_tree_path, idx],
                                ERR_INPUT_SCHEMA_ENUM_INVALID_TYPE,
                                value_erroneous=item,
                            )
                        )

        # Dictionary
        else:
            # Empty ref, shouldn't be the case, except for the root that may be
            if len(ref) == 0 and len(current_tree_path) > 0:
                schema_errors.append(
                    ErrorJson(
                        current_tree_path,
                        ERR_INPUT_SCHEMA_DICT_EMPTY,
                        value_erroneous=ref,
                    )
                )

            # Iterate over input schema entries
            for schema_key, schema_value in ref.items():
                helper(schema_value, [*current_tree_path, schema_key])

    helper(schema_input, [])

    return schema_errors


def detect_errors_in_output_json(
    schema_input: dict | list | str,
    output: dict | list | str,
    text_input: str | list[str] | None,
    leaf_types: Mapping[str, type] = NUEXTRACT_DEFAULT_TYPES,
) -> list[ErrorJson]:
    """
    Recursively check that a structured output follows an input schema.

    The method recursively checks that the keys in the two dictionaries are identical
    and inserted in the same order.

    The leaf types, country names and currency codes are provided as arguments in order
    to allow changes across versions.

    :param schema_input: input schema to follow.
    :param output: output schema to check.
    :param text_input: text input to extract the information from the schema from.
        (default: ``None``)
    :param leaf_types: dictionary mapping leaf types names to the associated expected
        Python type (default: ``TYPE_NAME_TO_TYPE``).
    :return: the errors in the output, as a lists of tuples containing the paths
        to the error in the schema and the error message.
    """
    # [((node_name), error_msg)]
    output_errors = []

    # Filter out non JSON-serializable samples
    output_can_be_a_string_leaf = (
        isinstance(schema_input, str) and schema_input in leaf_types
    ) or is_object_enum(schema_input)
    if isinstance(schema_input, str) and schema_input not in leaf_types:
        try:
            schema_input = orjson.loads(schema_input)
        except JSONDecodeError as e:
            raise ValueError(
                _ := "Input schema should be JSON serializable and cannot be repaired"
            ) from e
    # For labels
    if isinstance(output, str) and not output_can_be_a_string_leaf:
        try:
            output = orjson.loads(output)
        except JSONDecodeError:
            return [ErrorJson([], ERR_LABEL_NOT_JSON_DESERIALIZABLE)]

    # Perform a copy to prevent from unwanted inplace modifications that may be
    # performed when checking the schemas by the method to be applied on the original
    # objects/dictionaries.
    output = deepcopy(output)

    def helper(ref, pred, current_tree_path: list[str]) -> None:  # noqa: ANN001
        # Base case
        if not isinstance(ref, (dict, list)):
            err = _base_case_validation(ref, pred, leaf_types, text_input)
            if err is not None:
                output_errors.append(
                    ErrorJson(current_tree_path, err, value_erroneous=pred)
                )

        # Ref is a dict or a list, this pred node is not expected to be null except
        # for enums
        elif pred is None:
            # Pred is null but should have been a dict/branch
            if isinstance(ref, dict):
                output_errors.append(
                    ErrorJson(
                        current_tree_path,
                        ERR_LABEL_ARRAY_VALUE_IS_NULL_INSTEAD_OF_EMPTY_DICT,
                        value_erroneous=pred,
                    )
                )
            # Pred is null but should have been an array/multi-enum res
            elif not is_object_enum(ref):
                output_errors.append(
                    ErrorJson(
                        current_tree_path,
                        ERR_LABEL_ARRAY_VALUE_IS_NULL_INSTEAD_OF_EMPTY_ARR,
                        value_erroneous=pred,
                    )
                )

        # Ref/Pred not are the same type (dicts or arrays), except enums
        # != 1 so that an empty ref array doesn't match the condition, so that the error
        # is catched in the next if condition.
        elif not isinstance(ref, type(pred)) and not (
            isinstance(ref, list) and len(ref) != 1
        ):
            if isinstance(ref, dict):
                if isinstance(pred, list):
                    output_errors.append(
                        ErrorJson(
                            current_tree_path,
                            ERR_LABEL_NODE_VALUE_IS_ARRAY_INSTEAD_OF_DICT,
                            value_erroneous=pred,
                        )
                    )
                else:
                    output_errors.append(
                        ErrorJson(
                            current_tree_path,
                            ERR_LABEL_NODE_VALUE_IS_BASE_TYPE_INSTEAD_OF_DICT,
                            value_erroneous=pred,
                        )
                    )
            else:  # ref is list --> array of type
                if isinstance(pred, dict):
                    output_errors.append(
                        ErrorJson(
                            current_tree_path,
                            ERR_LABEL_NODE_VALUE_IS_DICT_INSTEAD_OF_ARRAY,
                            value_erroneous=pred,
                        )
                    )
                elif isinstance(ref[0], list) and not isinstance(pred, list):
                    output_errors.append(
                        ErrorJson(
                            current_tree_path,
                            ERR_LABEL_ARRAY_VALUE_IS_BASE_TYPE_INSTEAD_OF_ARRAY,
                            value_erroneous=pred,
                        )
                    )
                else:
                    output_errors.append(
                        ErrorJson(
                            current_tree_path,
                            ERR_LABEL_ARRAY_VALUE_IS_BASE_TYPE_INSTEAD_OF_ARRAY,
                            value_erroneous=pred,
                        )
                    )

        # Array: enum, multi-enum or array
        elif isinstance(ref, list):
            # enum
            if is_object_enum(ref):
                if isinstance(pred, list):
                    output_errors.append(
                        ErrorJson(
                            current_tree_path,
                            ERR_LABEL_ENUM_VALUE_IS_A_LIST_INSTEAD_OF_BASE_TYPE,
                            value_erroneous=pred,
                        )
                    )
                elif pred not in ref:
                    output_errors.append(
                        ErrorJson(
                            current_tree_path,
                            ERR_LABEL_ENUM_VALUE_NOT_IN_INPUT_SCHEMA,
                            value_erroneous=pred,
                        )
                    )
                return
            # From here, len(ref) == 1, either array of items or multi-enum
            # From here, multiple errors can be present for a single node
            # check for duplication (array or multi-enum)
            if len({str(pred_i) for pred_i in pred}) != len(pred):
                output_errors.append(
                    ErrorJson(
                        current_tree_path,
                        ERR_LABEL_ARRAY_HAS_DUPLICATED_ELEMENTS,
                        value_erroneous=pred,
                    )
                )
            # multi-enum
            if is_object_multi_enum(ref):
                if len(pred) > 0 and isinstance(pred[0], list):
                    output_errors.append(
                        ErrorJson(
                            current_tree_path,
                            ERR_LABEL_MULTI_ENUM_IS_LIST_OF_LIST,
                            value_erroneous=pred,
                        )
                    )
                    return
                for idx, item in enumerate(pred):
                    if item not in ref[0]:
                        output_errors.append(
                            ErrorJson(
                                [*current_tree_path, idx],
                                ERR_LABEL_MULTI_ENUM_VALUE_NOT_IN_INPUT_SCHEMA,
                                value_erroneous=item,
                            )
                        )
            # array of items -> check each item in pred
            else:
                # If ref is list of dict and pred is empty, still have to verify that
                # the ref dict leaf types are valid, so we mock the pred with a
                # nullified dict
                if isinstance(ref[0], dict) and len(pred) == 0:
                    # mock pred with dummy dict
                    # The ERR_LABEL_ARRAY_ITEM_IS_NULL error can be triggered because
                    # the mocked schema is empty/null. All label errors that may have
                    # been added are deleted after.
                    num_errors_labels_before = len(output_errors)
                    helper(ref[0], mock_schema(ref[0]), [*current_tree_path, 0])
                    while len(output_errors) != num_errors_labels_before:
                        del output_errors[-1]
                for idx, pred_i in enumerate(pred):
                    if is_item_null(pred_i):
                        output_errors.append(
                            ErrorJson(
                                [*current_tree_path, idx],
                                ERR_LABEL_ARRAY_ITEM_IS_NULL,
                                value_erroneous=pred_i,
                            )
                        )
                        # Still check the schema. If the list only contain one "null"
                        # dictionary, then the input schema would not be checked
                        # otherwise.
                        if isinstance(ref[0], dict):
                            num_errors_labels_before = len(output_errors)
                            helper(ref[0], mock_schema(ref[0]), [*current_tree_path, 0])
                            while len(output_errors) != num_errors_labels_before:
                                del output_errors[-1]
                        continue
                    helper(ref[0], pred_i, [*current_tree_path, idx])

        # Dictionary
        else:
            # Label keys not present in input schema
            output_errors.extend(
                ErrorJson(
                    [*current_tree_path, label_key],
                    ERR_LABEL_NODE_NOT_IN_INPUT_SCHEMA,
                    value_erroneous=label_key,
                )
                for label_key in pred
                if label_key not in ref
            )
            # Iterate over input schema entries
            for schema_key, schema_value in ref.items():
                if schema_key not in pred:
                    output_errors.append(
                        ErrorJson(
                            [*current_tree_path, schema_key],
                            ERR_LABEL_MISSING_NODE_FROM_INPUT_SCHEMA,
                        )
                    )
                    # Mock the pred so that the input schema is still checked
                    if not isinstance(schema_value, (dict, list)) or is_object_enum(
                        schema_value
                    ):
                        pred[schema_key] = None
                    else:
                        # The ERR_LABEL_ARRAY_ITEM_IS_NULL error can be triggered
                        # because the mocked schema is empty/null. All label errors that
                        # may have been added are deleted after.
                        num_errors_labels_before = len(output_errors)
                        helper(
                            schema_value,
                            mock_schema(schema_value),
                            [*current_tree_path, schema_key],
                        )
                        while len(output_errors) != num_errors_labels_before:
                            del output_errors[-1]
                        continue
                helper(schema_value, pred[schema_key], [*current_tree_path, schema_key])

    helper(schema_input, output, [])

    return output_errors


def is_item_null(item: object) -> bool:
    """
    Return a boolean indicating if an object is None, or empty.

    The method works recursively for lists and dictionaries by checking the values of
    their leaves, in which case it returns ``True`` only if all values are
    null/``None``.

    :param item: object to analyze.
    :return: whether the item is null/None or totally empty.
    """
    if item is None or (isinstance(item, list) and len(item) == 0):
        return True
    if isinstance(item, list):
        return all(is_item_null(value) for value in item)
    if not isinstance(item, dict):
        return False
    # Item is a dict, return True if all leaf values are null/empty
    return all(is_item_null(value) for value in item.values())
