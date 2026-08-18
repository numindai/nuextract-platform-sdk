"""Verbatim string type."""

from __future__ import annotations

from collections import Counter
from difflib import Match
from string import punctuation
from typing import TYPE_CHECKING, Literal

import regex
import stringzilla as sz
from cdifflib import CSequenceMatcher
from rapidfuzz.distance import Indel

from .base import SemanticType
from .string_ import (
    ERR_LABEL_LEAF_VALUE_NULL_STRING_INSTEAD_OF_NULL,
    ERRORS_STRING,
    String,
)

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson

NULL_STRINGS = {  # only for string, not applicable to enums
    "null",
    "none",
}
# \v and \0 are not supported in JSON
ESCAPE_CHARACTERS_NOT_IN_STRING = ("\r", "\b", "\f", "\v", "\0")
# All Unicode "space separators" (Zs), including NBSP, EM SPACE, THIN SPACE, etc.
UNICODE_SPACES = [
    "\u00a0",  # NBSP (non-breaking space)
    "\u2000",  # en quad
    "\u2001",  # em quad
    "\u2002",  # en space
    "\u2003",  # em space
    "\u2004",  # three-per-em space
    "\u2005",  # four-per-em space
    "\u2006",  # six-per-em space
    "\u2007",  # figure space
    "\u2008",  # punctuation space
    "\u2009",  # thin space
    "\u200a",  # hair space
    "\u202f",  # narrow no-break space
    "\u205f",  # medium mathematical space
    "\u3000",  # ideographic space
]

# Unicode ranges for each relevant script
UNICODE_RANGES_LANGUAGES_WITHOUT_SPACES = [
    r"\u4E00-\u9FFF",  # CJK Unified Ideographs (Chinese characters)
    r"\u3400-\u4DBF",  # CJK Unified Ideographs Extension A
    r"\u3040-\u309F",  # Hiragana (Japanese)
    r"\u30A0-\u30FF",  # Katakana (Japanese)
    r"\uAC00-\uD7AF",  # Hangul Syllables (Korean, can also be relevant in some cases)
    r"\u0E00-\u0E7F",  # Thai
    r"\u0ED0-\u0EFF",  # Lao digits and symbols
    r"\u0E80-\u0EFF",  # Lao (covers full Lao script)
    r"\u1780-\u17FF",  # Khmer
    r"\u1000-\u109F",  # Burmese (Myanmar)
    r"\u0F00-\u0FFF",  # Tibetan
    r"\uA980-\uA9DF",  # Javanese
    r"\u1B00-\u1B7F",  # Balinese
]
UNICODE_RANGES_LANGUAGES_WITHOUT_SPACES_PATTERN = (
    "[" + "".join(UNICODE_RANGES_LANGUAGES_WITHOUT_SPACES) + "]"
)

# Word splitting regex
SCRIPT_SEGMENT_PATTERN = regex.compile(
    r"\p{Han}+|"  # Chinese characters
    r"\p{Hiragana}+|"  # Japanese hiragana
    r"\p{Katakana}+|"  # Japanese katakana
    r"\p{Hangul}+|"  # Korean
    r"\p{Thai}+|"  # Thai
    r"\p{Khmer}+|"  # Khmer
    r"\p{Lao}+|"  # Lao
    r"\p{Myanmar}+|"  # Burmese
    # Everything else
    r"[^\p{Han}\p{Hiragana}\p{Katakana}\p{Hangul}\p{Thai}\p{Khmer}\p{Lao}\p{Myanmar}]+"
)
SCRIPTS_CHECK = [
    ("Han", r"\p{Han}"),
    ("Hiragana", r"\p{Hiragana}"),
    ("Katakana", r"\p{Katakana}"),
    ("Hangul", r"\p{Hangul}"),
    ("Thai", r"\p{Thai}"),
    ("Khmer", r"\p{Khmer}"),
    ("Lao", r"\p{Lao}"),
    ("Myanmar", r"\p{Myanmar}"),
    ("Arabic", r"\p{Arabic}"),
    ("Hebrew", r"\p{Hebrew}"),
    ("Cyrillic", r"\p{Cyrillic}"),
    ("Devanagari", r"\p{Devanagari}"),
    ("Bengali", r"\p{Bengali}"),
    ("Gujarati", r"\p{Gujarati}"),
    ("Tamil", r"\p{Tamil}"),
    ("Greek", r"\p{Greek}"),
]
UNIVERSAL_TOKENIZE_PATTERN = regex.compile(
    r"\p{L}\d+(?:\.\d+)+|"  # Version numbers like v1.2.3
    r"\d+(?:\.\d+)+|"
    r"[\p{L}\p{M}\d]+"
)
SCRIPT_TOKENIZE_PATTERNS = {
    "Han": regex.compile(r"\p{Han}+"),
    "Hiragana": regex.compile(r"\p{Hiragana}+"),
    "Katakana": regex.compile(r"\p{Katakana}+"),
    "Hangul": regex.compile(r"\p{Hangul}+"),
    "Thai": regex.compile(r"\p{Thai}+"),
    "Khmer": regex.compile(r"\p{Khmer}+"),
    "Lao": regex.compile(r"\p{Lao}+"),
    "Myanmar": regex.compile(r"\p{Myanmar}+"),
}

# Constants used to validate a verbatim string fix.
# One of these two limits must be met to validate a fixes verbatim string. Using both
# allows to validate fixes on short substrings, for example "map" --> "mat" which is a
# desirable and common case is ratio 0.33 but indel 2
# Maximum indel ratio to meet to validate a fix
VERBATIM_STRING_FIX_INDEL_RATIO_THRESHOLD = 0.25
# Above this indel ratio, the value is "fixed" by being set to null. Below, it is either
# fixed if < VERBATIM_STRING_FIX_INDEL_RATIO_THRESHOLD or the node is deleted to
# avoid false negative ("false" null values)
VERBATIM_STRING_FIX_INDEL_RATIO_SET_TO_NULL = 0.50
# Maximum indel distance to meet to validate a fix.
VERBATIM_STRING_FIX_MAX_INDEL_DISTANCE_OK = 2  # one char replacement
MAX_LENGTH = 4000

ERR_LABEL_VERBATIM_STRING_CONTAIN_INVALID_ESCAPE_CHARACTERS = (
    'label verbatim-string value contain invalid escape characters ("\\r", "\\b"...)'
)
ERR_LABEL_VERBATIM_STRING_ABSENT_FROM_INPUT = (
    "label verbatim-string value is not present in the input"
)
ERR_LABEL_VERBATIM_STRING_IN_INPUT_BUT_LETTER_CASE_NOT_RESPECTED = (
    "label verbatim-string value is present in the input but does not respect the "
    "letter case (case insensitive)"
)
ERR_LABEL_IS_NOT_NULL_WHEREAS_INPUT_TEXT_IS = (
    "label value verbatim is not `None` whereas the input text is"
)
ERR_LABEL_VALUE_IS_TOO_LONG = "label value verbatim-string is too long"


class VerbatimString(SemanticType):
    """
    A `string` as it strictly is in the input.

    This type is purely extractive as the string should be present exactly as it is in
    the input, preserving all characters including accents, symbols, emojis or any
    unicode character. The verbatim string shouldn’t contain new lines, tabs or multiple
    consecutive white spaces. These elements should be represented with one white space.

    :examples: `John Doe`, `1120 Santa Monica Boulevard`
    """  # noqa:RUF002

    ratio_max_fixable: float = VERBATIM_STRING_FIX_INDEL_RATIO_THRESHOLD
    ratio_min_set_to_null: float = VERBATIM_STRING_FIX_INDEL_RATIO_SET_TO_NULL
    fix_max_indel_distance_ok: int = VERBATIM_STRING_FIX_MAX_INDEL_DISTANCE_OK
    max_length: int = MAX_LENGTH
    fix_on_words: bool = True

    @classmethod
    def coerce(
        cls,
        value: str,
        input_text: str | list[str] | None = None,
        error: ErrorJson | None = None,
    ) -> str | None:
        """
        Try to convert a value to its string type.

        :param value: value to convert to string if it can, otherwise ``None``.
        :param input_text: input text from which the value is expected to be found
            verbatim (default: ``None``).
        :param error: error associated to the value to convert. This argument
            can help to convert the value by targeting to the appropriate methods
            (default: ``None``).
        :return: a string value found verbatim in the input text.
        """
        # No error, just return the value with no further validation
        if error is None:
            return value

        # Convert to string
        if not isinstance(value, str):
            return str(value)

        # Null or unfixable value
        if error.error_message in (
            ERR_LABEL_IS_NOT_NULL_WHEREAS_INPUT_TEXT_IS,
            ERR_LABEL_VALUE_IS_TOO_LONG,
        ):
            return None

        # Value is not a string, try to convert it first then check if it is verbatim
        if error.error_message in ERRORS_STRING:
            value_fixed = String(value, error=error)
            if value_fixed is None:
                return None
            value = value_fixed
            err_verbatim = VerbatimString.validate(value, input_text)
            if err_verbatim is None:
                return value
            error.error_message = err_verbatim

        # String contain invalid escape character(s) --> remove them
        if (
            error.error_message
            == ERR_LABEL_VERBATIM_STRING_CONTAIN_INVALID_ESCAPE_CHARACTERS
        ):
            for char in ESCAPE_CHARACTERS_NOT_IN_STRING:
                value = value.replace(char, "")
            return value

        # Prepare input_text
        if isinstance(input_text, str):
            input_text = [input_text]
        input_text = [
            _convert_string_to_comply_with_verbatim_string(text) for text in input_text
        ]
        value = _convert_string_to_comply_with_verbatim_string(value)

        # Verbatim string present but with invalid letter case
        if (
            error.error_message
            == ERR_LABEL_VERBATIM_STRING_IN_INPUT_BUT_LETTER_CASE_NOT_RESPECTED
        ):
            if isinstance(input_text, str):
                input_text = [input_text]
            for text in input_text:
                if text.lower().find(value.lower()) != -1:
                    return convert_substring_to_match_case(text, value)
            return None  # Shouldn't happen if validation was correct

        # Verbatim string absent from input text --> try to "verbatimize"
        if error.error_message == ERR_LABEL_VERBATIM_STRING_ABSENT_FROM_INPUT:
            # If we have a list, try to find the best match in ONE of the strings
            if isinstance(input_text, list):
                corrected_substring = find_closest_verbatim_string_in_list(
                    input_text, value, word_level=cls.fix_on_words
                )
            else:
                # character-level if language without spaces, otherwise word-level
                corrected_substring = find_closest_verbatim_string(
                    input_text,
                    value,
                    word_level=cls.fix_on_words and not contains_no_space_script(value),
                )
            original_fixed_distance = Indel.distance(value, corrected_substring)
            original_fixed_distance_ratio = original_fixed_distance / (
                len(value) + len(corrected_substring)
            )
            if (
                original_fixed_distance_ratio <= cls.ratio_max_fixable
                or original_fixed_distance <= cls.fix_max_indel_distance_ok
            ):
                return corrected_substring
            if original_fixed_distance_ratio <= cls.ratio_min_set_to_null:
                error.node_deleted = True

        return None

    @classmethod
    def validate(
        cls, value: str, text_input: str | list[str] | None = None
    ) -> str | None:
        """
        Check that a string is indeed verbatim to the input text.

        :param value: string value to assess.
        :param text_input: input text from which the value is expected to be found
            verbatim (default: ``None``).
        :return: error message if the value is not in the input text, otherwise
            ``None``.
        """
        # Allow verbatim string value to be string "null"
        if (err_string := String.validate(value)) not in {
            None,
            ERR_LABEL_LEAF_VALUE_NULL_STRING_INSTEAD_OF_NULL,
        }:
            return err_string

        if text_input is None:
            return None
        # Handle list of strings
        if isinstance(text_input, str):
            text_input = [text_input]
        # Check if all texts are empty
        if all(text.strip() == "" for text in text_input):
            return ERR_LABEL_IS_NOT_NULL_WHEREAS_INPUT_TEXT_IS

        # Check length
        if len(value) > cls.max_length:
            return ERR_LABEL_VALUE_IS_TOO_LONG

        # Try to find the value in any of the strings
        verbatim_error = ERR_LABEL_VERBATIM_STRING_ABSENT_FROM_INPUT
        case_insensitive_found = None

        for text in text_input:
            text_formatted = _convert_string_to_comply_with_verbatim_string(text)
            item_error = is_verbatim_string_valid(value, text_formatted)

            if item_error is None:
                # Found verbatim in one of the strings
                return None
            if (
                item_error
                == ERR_LABEL_VERBATIM_STRING_CONTAIN_INVALID_ESCAPE_CHARACTERS
            ):
                return item_error
            if (
                item_error
                == ERR_LABEL_VERBATIM_STRING_IN_INPUT_BUT_LETTER_CASE_NOT_RESPECTED
            ):
                case_insensitive_found = text_formatted

        # If found with case mismatch, return that error; otherwise absent
        if case_insensitive_found:
            # TODO report fixed value?
            return ERR_LABEL_VERBATIM_STRING_IN_INPUT_BUT_LETTER_CASE_NOT_RESPECTED

        return verbatim_error


def is_verbatim_string_valid(verbatim_string: str, text_input: str) -> str | None:
    r"""
    Check that a string is valid to be in the benchmark data.

    If any newline (``"\n"``) or return carriage (``"\r"``) is present in the string,
    it is considered non-valid.

    This method uses stringzilla to make the substring search process a bit faster.

    :param verbatim_string: string to validate.
    :param text_input: text input to extract the information from the schema from.
        It should be formatted to comply with the verbatim-string type.
        (default: ``None``)
    :return: error message in case the string is not considered verbatim.
    """
    if any(
        sz.contains(verbatim_string, item) for item in ESCAPE_CHARACTERS_NOT_IN_STRING
    ):
        return ERR_LABEL_VERBATIM_STRING_CONTAIN_INVALID_ESCAPE_CHARACTERS
    if not sz.contains(text_input, verbatim_string):
        if sz.contains(text_input.lower(), verbatim_string.lower()):
            return ERR_LABEL_VERBATIM_STRING_IN_INPUT_BUT_LETTER_CASE_NOT_RESPECTED
        return ERR_LABEL_VERBATIM_STRING_ABSENT_FROM_INPUT
    return None


def _get_ratio_words_not_in(value: str, text_input: str) -> float:
    # Measure ratio of word presence
    words_input = set(smart_tokenize(text_input))
    words_leaf = smart_tokenize(value)
    words_in = [word for word in words_leaf if word in words_input]
    return (len(words_leaf) - len(words_in)) / len(words_leaf)


def smart_tokenize(text: str) -> list[str]:
    """
    Tokenize a text into distinct words.

    Handles mixed-script text by segmenting first, then tokenizing each segment.

    :param text: text to tokenize.
    :return: list of words in the text.
    """
    if not text:
        return []

    # Segment text by script boundaries
    segments = []
    for match in SCRIPT_SEGMENT_PATTERN.finditer(text):
        segment_text = match.group(0)
        if segment_text.strip():
            segments.append(segment_text)

    # Tokenize each segment
    all_tokens = []
    for segment in segments:
        script = _detect_script_fast(segment)
        tokens = _tokenize_segment(segment, script)
        all_tokens.extend(tokens)

    return all_tokens


def _detect_script_fast(text: str) -> str | None:
    """Detect script in text using regex, returns ISO 15924 script code."""
    if not text or not text.strip():
        return None

    # Check for specific scripts first (these are unambiguous)
    script_counts = Counter()

    for script_name, pattern in SCRIPTS_CHECK:
        count = len(regex.findall(pattern, text))
        if count > 0:
            script_counts[script_name] += count

    # If no specific script found, assume Latin
    if not script_counts:
        if regex.search(r"\p{Latin}", text):
            return "Latn"
        return None

    # Return most common script
    dominant_script = script_counts.most_common(1)[0][0]

    return dominant_script if dominant_script is not None else "Latn"


def _tokenize_segment(text: str, script: str | None = None) -> list[str]:
    """Tokenize a text segment based on its script."""
    if not text or not text.strip():
        return []

    # For scripts without word boundaries, use script-specific patterns
    if script in SCRIPT_TOKENIZE_PATTERNS:
        pattern = SCRIPT_TOKENIZE_PATTERNS[script]
        tokens = [m.group(0) for m in pattern.finditer(text)]
        return [t for t in tokens if t.strip()]

    # For spaced scripts (Latin, Cyrillic, etc.), use universal pattern
    tokens = [m.group(0) for m in UNIVERSAL_TOKENIZE_PATTERN.finditer(text)]
    return [t for t in tokens if t.strip()]


def _convert_string_to_comply_with_verbatim_string(text_input: str) -> str:
    """Convert a text input to the verbatim string formatting."""
    for escape_char in ESCAPE_CHARACTERS_NOT_IN_STRING:
        text_input = text_input.replace(escape_char, " ")
    # Convert all space-like Unicode characters (except newline) into ASCII space
    for space_char in UNICODE_SPACES:
        text_input = text_input.replace(space_char, " ")
    # Collapse multiple ASCII spaces into one (without touching newlines)
    text_input = regex.sub(r" {2,}", " ", text_input)
    # import string  # uncomment to measure against without punctuation
    # translator = str.maketrans('', '', string.punctuation)
    # text_input = text_input.translate(translator)
    # Specifying " " so that it doesn't split on newline characters "\n"
    return text_input.strip()


def convert_substring_to_match_case(input_text: str, substring: str) -> str:
    """
    Convert the letter case of a string to match its corresponding substring in a text.

    :param input_text: The reference string containing the pattern with desired case.
    :param substring: The string to be converted (a case-insensitive substring of
        ``input_text``).
    :return: The ``substring`` with letter case matching the corresponding section in
        ``input_text``. Returns the original ``substring`` if no match is found.
    """
    # Convert both strings to lowercase for case-insensitive matching
    large_lower = input_text.lower()
    substring_lower = substring.lower()

    # Find the position of small_string in large_string (case-insensitive)
    start_pos = large_lower.find(substring_lower)

    # If the small string isn't found in the large string, return original small string
    if start_pos == -1:
        return substring

    # Extract the corresponding substring from large_string with original case
    corresponding_substring = input_text[start_pos : start_pos + len(substring)]
    # TODO len(substring) might differ from len(corresponding_substring)

    # Apply the case pattern from the corresponding substring to small_string
    result = ""
    for i in range(len(corresponding_substring)):
        if corresponding_substring[i].isupper():
            result += substring[i].upper()
        else:
            result += substring[i].lower()

    # TODO might not work with specific string encodings. Maybe comes from the fact that
    #  the string search error was spotted with stringzilla for which results might diff
    # if result not in input_text:
    #    t = 0
    return result


def _string_search(
    text: str,
    query: str,
    pos_start_query_in_text: int,
    max_indel_dist: int,
    direction: Literal["left", "right"],
) -> str:
    best = ""
    best_dist = len(query)
    range_ = (
        range(pos_start_query_in_text - 1, -1, -1)
        if direction == "left"
        else range(pos_start_query_in_text + 1, len(text) + 1)
    )
    for idx in range_:
        temp_str = (
            text[idx:pos_start_query_in_text]
            if direction == "left"
            else text[pos_start_query_in_text:idx]
        )
        # Limit search to reasonable length
        if len(temp_str) > max_indel_dist:
            break
        temp_indel_dist = Indel.distance(temp_str, query)
        # Update if we found a better match or same distance but longer match
        if temp_indel_dist < best_dist or (
            temp_indel_dist == best_dist and len(temp_str) > len(best)
        ):
            best_dist = temp_indel_dist
            best = temp_str

    return best


def _get_incomplete_word_from_substring(
    text: str,
    substring: str,
    idx_start_substring_in_text: int,
    direction: Literal["left", "right"],
    return_extended_substring: bool = True,
) -> str:
    words_in_substring = substring.split()
    complete_word = _get_word_in_str_at_idx(text, idx_start_substring_in_text)
    if direction == "left":
        word_to_complete = words_in_substring[0]
        if not complete_word.endswith(word_to_complete):
            word_to_complete += _extract_substring(
                complete_word, word_to_complete, "right"
            )
        pre_suf_fix = complete_word.removesuffix(word_to_complete)
    else:
        word_to_complete = words_in_substring[-1]
        if not complete_word.startswith(word_to_complete):
            word_to_complete = (
                _extract_substring(complete_word, word_to_complete, "left")
                + word_to_complete
            )
        pre_suf_fix = complete_word.removeprefix(word_to_complete)

    if return_extended_substring:
        return (
            pre_suf_fix + substring if direction == "left" else substring + pre_suf_fix
        )
    return pre_suf_fix


def _extract_substring(
    string: str, substring: str, direction: Literal["left", "right"]
) -> str:
    # Find the starting position of substring in large_string
    start_pos = string.find(substring)
    end_pos = start_pos + len(substring)

    # Return the part before or after substring based on direction
    if direction.lower() == "left":
        return string[:start_pos]
    return string[end_pos:]


def _get_word_in_str_at_idx(string: str, index: int) -> str:
    words = string.split()
    word_at_index = words[0]
    cum_words_start_idx = 0
    if len(words) > 0:
        for idx, word in enumerate(words):
            if idx == 0:
                continue
            cum_words_start_idx = cum_words_start_idx + 1 + len(words[idx - 1])
            if cum_words_start_idx > index:
                break
            word_at_index = word

    return word_at_index


def find_closest_verbatim_string(
    text: str, substring: str, word_level: bool = False
) -> str:
    """
    Perform fuzzy text search to find the best matching substring.

    Uses a three-part approach:
    1. Find the longest common substring/word sequence as an anchor;
    2. Expand left of the anchor to match the query's left part;
    3. Expand right of the anchor to match the query's right part.

    If using word-level, the corrected substring will feature only untrimmed words,
    unless the longest common contiguous subsequence is starts/ends in the same word as
    the ``substring`` in which case the starting/ending words are included.

    :param text: The reference string containing the pattern with desired case.
    :param substring: The malformed substring to make a contiguous substring from the
        ``text``.
    :param word_level: If ``True``, perform matching at word level instead of character
        level.
    :return: contiguous substring from the ``text``.
    """
    # Original character-level implementation
    matcher = CSequenceMatcher(None, text, substring)
    match = matcher.find_longest_match(0, len(text), 0, len(substring))
    if match.size == 0:
        return ""

    # Create lcs and strip leading/trailing spaces
    lcs = text[match.a : match.a + match.size]
    if lcs[0] == " ":
        lcs = lcs[1:]
        match = Match(match.a + 1, match.b + 1, match.size - 1)
        if match.size == 0:
            return ""

    if lcs[-1] == " ":
        lcs = lcs[:-1]
        match = Match(match.a, match.b, match.size - 1)
        if match.size == 0:
            return ""

    # Step 2: Search left side
    if match.b == 0:
        left_best = ""
    else:
        left_query = substring[: match.b]
        left_best = _string_search(
            text, left_query, match.a, 2 * len(left_query), "left"
        )
        if word_level:
            idx_in_text_with_best = match.a - len(left_best)
            # If not beginning of text and previous char isn't a space or newline
            if idx_in_text_with_best > 0 and text[idx_in_text_with_best - 1] not in (
                " ",
                "\n",
            ):
                # If left_best + lcs starts in middle of a word, remove the leading
                # word unless it is in lcs
                if " " in left_best or "\n" in left_best:
                    # Find the last space or newline to remove incomplete leading word
                    last_space = left_best.rfind(" ")
                    last_newline = left_best.rfind("\n")
                    last_boundary = max(last_space, last_newline)
                    if last_boundary >= 0:
                        left_best = left_best[last_boundary + 1 :]
                    else:
                        left_best = ""
                else:
                    left_best = _get_incomplete_word_from_substring(
                        text,
                        lcs,
                        idx_in_text_with_best,
                        "left",
                        return_extended_substring=False,
                    )

    # Step 3: Search right side
    if match.b + match.size == len(substring):
        right_best = ""
    else:
        right_query = substring[match.b + match.size :]
        right_best = _string_search(
            text, right_query, match.a + match.size, 2 * len(right_query), "right"
        )
        if word_level:
            idx_in_text_with_best = match.a + match.size + len(right_best)
            # If not beginning of text and previous char isn't a space or newline
            if idx_in_text_with_best > 0 and text[idx_in_text_with_best - 1] not in (
                " ",
                "\n",
            ):
                # If lcs + best ends in middle of a word, remove the trailing
                # word unless it is in lcs
                if " " in right_best or "\n" in right_best:
                    # Find the first space or newline to remove incomplete trailing word
                    first_space = right_best.find(" ")
                    first_newline = right_best.find("\n")
                    # Get the first boundary (ignoring -1 which means not found)
                    boundaries = [b for b in [first_space, first_newline] if b >= 0]
                    if boundaries:
                        first_boundary = min(boundaries)
                        right_best = right_best[:first_boundary]
                    else:
                        right_best = ""
                else:
                    right_best = _get_incomplete_word_from_substring(
                        text,
                        lcs,
                        idx_in_text_with_best,
                        "right",
                        return_extended_substring=False,
                    )

    # Combine all parts: left match + center anchor + right match
    substring_corrected = (left_best + lcs + right_best).strip()

    # Discard trailing punctuation
    start_index = 0
    while (
        start_index < len(substring_corrected)
        and substring_corrected[start_index] in punctuation
    ):
        start_index += 1
    end_index = len(substring_corrected) - 1
    while end_index >= 0 and substring_corrected[end_index] in punctuation:
        end_index -= 1

    # Return the string between the first and last non-punctuation characters
    # If the string is all punctuation, this will return an empty string
    if start_index > end_index:
        return ""

    return substring_corrected[start_index : end_index + 1]


def find_closest_verbatim_string_in_list(
    text_list: list[str], substring: str, word_level: bool = False
) -> str:
    """
    Find the best matching substring within one of the text strings.

    Tries each string in the list independently and returns the best match based on edit
    distance. The returned substring is guaranteed to be entirely within a single text
    string (no spanning across texts).

    :param text_list: List of reference strings
    :param substring: The malformed substring to correct
    :param word_level: If True, perform matching at word level
    :return: Best matching contiguous substring found within one of the texts
    """
    if not text_list:
        return ""

    best_match = ""
    best_distance = float("inf")

    # Try to find match in each text independently
    for text in text_list:
        candidate = find_closest_verbatim_string(text, substring, word_level)
        if candidate:
            distance = Indel.distance(substring, candidate)
            # Update if this is a better match
            if distance < best_distance:
                best_distance = distance
                best_match = candidate

    return best_match


def contains_no_space_script(text: str) -> bool:
    """
    Detect if a string contains characters from alphabets of languages without spaces.

    :param text: string to assess.
    :return: whether the text contains characters from alphabets of languages that
        typically doesn't use spaces.
    """
    # Compile one big regex pattern from all ranges
    return bool(regex.search(UNICODE_RANGES_LANGUAGES_WITHOUT_SPACES_PATTERN, text))
