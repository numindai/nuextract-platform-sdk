"""Constants for errors."""

# JSON serialization errors
ERR_INPUT_SCHEMA_NOT_JSON_DESERIALIZABLE = (
    "input schema JSON is not deserializable / RFC 8259 compliant"
)
ERR_LABEL_NOT_JSON_DESERIALIZABLE = (
    "output JSON is not deserializable / RFC 8259 compliant"
)
# Input schema errors
ERR_INPUT_SCHEMA_LEAF_TYPE_INVALID = "input schema leaf type not in predefined types"
ERR_INPUT_SCHEMA_DICT_EMPTY = "input schema dictionary is empty"
ERR_INPUT_SCHEMA_ENUM_INVALID_TYPE = "input schema enum contain non-string values"
ERR_INPUT_SCHEMA_ARRAY_IS_EMPTY = "input schema array is empty"
# Label schema errors
ERR_LABEL_LEAF_TYPE_INVALID = "leaf value type is not valid"
ERR_LABEL_MISSING_NODE_FROM_INPUT_SCHEMA = "node from the input schema is missing"
ERR_LABEL_NODE_NOT_IN_INPUT_SCHEMA = "node not in input schema (non-existing node name)"
ERR_LABEL_LEAF_VALUE_IS_NOT_NULL_WHEREAS_INPUT_TEXT_IS = (
    "leaf value is not null whereas the input text is an empty string"
)
ERR_LABEL_ARRAY_VALUE_IS_NULL_INSTEAD_OF_EMPTY_DICT = (
    "array value is null instead of nullified dict `{: null, ...}`"
)
ERR_LABEL_ARRAY_VALUE_IS_NULL_INSTEAD_OF_EMPTY_ARR = (
    "array value is null instead of empty array `[]`"
)
ERR_LABEL_ARRAY_ITEM_IS_NULL = "array item is null (null shouldn't be in the array)"
ERR_LABEL_ARRAY_VALUE_IS_BASE_TYPE_INSTEAD_OF_ARRAY = (
    "array value is base type instead of an array"
)
ERR_LABEL_NODE_VALUE_IS_BASE_TYPE_INSTEAD_OF_DICT = (
    "node value is base type instead of a dict"
)
ERR_LABEL_NODE_VALUE_IS_ARRAY_INSTEAD_OF_DICT = (
    "node value is an array instead of a dictionary"
)
ERR_LABEL_NODE_VALUE_IS_DICT_INSTEAD_OF_ARRAY = (
    "node value is a dictionary instead of an array"
)
ERR_LABEL_ENUM_VALUE_IS_A_LIST_INSTEAD_OF_BASE_TYPE = (
    "enum/classification value is a list instead of base type"
)
ERR_LABEL_ENUM_VALUE_NOT_IN_INPUT_SCHEMA = (
    "enum/classification value not in input schema"
)
ERR_LABEL_ARRAY_HAS_DUPLICATED_ELEMENTS = "array has duplicated element(s)"
ERR_LABEL_MULTI_ENUM_IS_LIST_OF_LIST = (
    "multi-enum leaf value is a list of list instead of just a list"
)
ERR_LABEL_MULTI_ENUM_VALUE_NOT_IN_INPUT_SCHEMA = (
    "multi-enum value(s) not in input schema"
)

# Constants for schema fixes
INDEL_THRESHOLD_INPUT_TYPE = 2
INDEL_THRESHOLD_OUTPUT_ENUM = 2
INDEL_THRESHOLD_OUTPUT_NODE_NAME = 2


# Names for "constructors"
ARRAY_NAME = "array"
ENUM_NAME = "enum"
MULTI_ENUM_NAME = "multi-enum"
CONSTRUCTURE_TYPES_NAMES = {ARRAY_NAME, ENUM_NAME, MULTI_ENUM_NAME}
