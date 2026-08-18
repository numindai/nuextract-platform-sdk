"""Phone number type."""

from __future__ import annotations

import contextlib
import re
from collections import Counter
from typing import TYPE_CHECKING

import phonenumbers

from .base import SemanticType

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson

INDEL_WEIGHTS = (2, 2, 1)

ERR_LABEL_PHONE_NUMBER_CANNOT_BE_PARSED = (
    "label leaf phone number value cannot be parsed or is not valid"
)
ERR_LABEL_PHONE_NUMBER_CAN_BE_PARSED_BUT_IS_INVALID = (  # can't be fixed
    "label leaf phone number value can be parsed but is not valid"
)
ERR_LABEL_PHONE_NUMBER_IS_VALID_BUT_NOT_E164 = (
    "label leaf phone number value is valid but is not E.164 format"
)
ERR_LABEL_PHONE_NUMBER_IS_VALID_BUT_IN_MESSY_STRING = (
    "label leaf phone number value is valid but is in messy string"
)


"""COUNTRY_TO_LANGUAGES = defaultdict(list)
LANGUAGES_TO_COUNTRIES = defaultdict(list)
# Using the CLDR likely subtags file to infer languages covered by each script
# https://cldr.unicode.org/index/downloads
with (
    importlib.resources.files("numind.nuextract_utils._iso_data")
    .joinpath("CLDR supplementalData.xml")
    .open("rb") as _file
):
    tree = ElementTree.parse(_file)
    root = tree.getroot()
    likely_subtags = root.find("languageData")

    for elem in likely_subtags.findall("language"):
        language_iso639_1 = elem.attrib.get("type")
        countries_iso3166_1 = elem.attrib.get("territories")
        # Discard secondary usages
        if (alt_ := elem.attrib.get("alt")) is not None and alt_ == "secondary":
            continue
        # We're interested in entries where the 'to' has at least a script subtag
        if countries_iso3166_1 is not None:
            for country_code_ in countries_iso3166_1.split():
                COUNTRY_TO_LANGUAGES[country_code_].append(language_iso639_1)
                LANGUAGES_TO_COUNTRIES[language_iso639_1].append(country_code_)"""


class PhoneNumber(SemanticType):
    """
    A phone number.

    If the region code (e.g. +1 for the United States and Canada) is present or can be
    inferred, the string complies to the ITU E.164 standard, e.g. `+14155552671`.
    Otherwise, the string only contains digits and is as close as present in the input
    document, e.g. a phone number appearing as `650.555.0123` is extracted as
    `6505550123`. If the value is E.164 compliant (with region code), it is also
    necessarily diallable. For example, `+14155552671` is syntactically E.164 compliant
    but is not diallable, so not valid.

    :examples: `+33612345678` (French mobile), `6505550123` (US local without country
    code)
    """

    json_schema_format = ("phone-number-E.164", "phone-number")

    @classmethod
    def coerce(
        cls, value: str, input_text: str | None = None, error: ErrorJson | None = None
    ) -> str | None:
        """
        Try to convert a value to its string type.

        :param value: value to convert to string if it can, otherwise ``None``.
        :param input_text: input text.
        :param error: error associated to the value to convert. This argument
            can help to convert the value by targeting to the appropriate methods
            (default: ``None``).
        :return: a string value found verbatim in the input text.
        """
        _ = input_text
        if error is None:
            return value

        # Either an invalid number that cannot be fixed or a string from which no valid
        # NSN or E.164 number can be extracted, just return None without trying anything
        if error.error_message in {
            ERR_LABEL_PHONE_NUMBER_CAN_BE_PARSED_BUT_IS_INVALID,
            ERR_LABEL_PHONE_NUMBER_CANNOT_BE_PARSED,
        }:
            return None

        # Try direct parsing (region code must be present)
        with contextlib.suppress(phonenumbers.NumberParseException):
            phone_number = phonenumbers.parse(value)
            # If the number can be parsed, the country code is good so it shouldn't be
            # matched against others.
            # if not phonenumbers.is_valid_number(phone_number):
            #     return None
            return phonenumbers.format_number(
                phone_number, phonenumbers.PhoneNumberFormat.E164
            )

        # Try parsing in messy string (region code must be present)
        for match in phonenumbers.PhoneNumberMatcher(value, region=None):
            if phonenumbers.is_valid_number(number := match.number):
                return phonenumbers.format_number(
                    number, phonenumbers.PhoneNumberFormat.E164
                )

        # Try with possible region codes
        value_fixed = normalize_phone_number(value)
        # Convert to string if PhoneNumber object
        if isinstance(value_fixed, phonenumbers.PhoneNumber):
            value_fixed = phonenumbers.format_number(
                value_fixed, phonenumbers.PhoneNumberFormat.E164
            )

        # Can be an E.164 string, NSN or None
        return value_fixed

    @classmethod
    def validate(cls, value: str, _: str | None = None) -> str | None:
        """
        Check that a phone number string is valid.

        :param value: string value to assess.
        :param _: placeholder for text_input.
        :return: error message if the value is not in the input text, otherwise
            ``None``.
        """
        # Try to parse it directly, assuming region code is provided
        with contextlib.suppress(phonenumbers.NumberParseException):
            phone_number = phonenumbers.parse(value)
            # Still accept "invalid" numbers, i.e. syntactically complies to E.164 but
            # isn't diallable, for example the +1 555 block which is reserved for
            # fictional use.
            # if not phonenumbers.is_valid_number(phone_number):
            #     return ERR_LABEL_PHONE_NUMBER_CAN_BE_PARSED_BUT_IS_INVALID
            # Check that the value is actually exactly E.164
            if (
                phonenumbers.format_number(
                    phone_number, phonenumbers.PhoneNumberFormat.E164
                )
                != value
            ):
                return ERR_LABEL_PHONE_NUMBER_IS_VALID_BUT_NOT_E164
            return None

        # Try with the matcher, i.e. extract from messy string
        for match in phonenumbers.PhoneNumberMatcher(value, region=None):
            if phonenumbers.is_valid_number(match.number):
                return ERR_LABEL_PHONE_NUMBER_IS_VALID_BUT_IN_MESSY_STRING

        # Check that a NSN or E.164 number can be extracted from the string, and that it
        value_fixed = normalize_phone_number(value)
        if isinstance(value_fixed, phonenumbers.PhoneNumber):
            value_fixed = phonenumbers.format_number(
                value_fixed, phonenumbers.PhoneNumberFormat.E164
            )
        if value_fixed is not None:
            # If the value is different, it means that it can be improved
            if value_fixed == value:
                return None
            return ERR_LABEL_PHONE_NUMBER_IS_VALID_BUT_IN_MESSY_STRING

        # If no valid NSN or E.164 number can be extracted/reformated from the provided
        # value, return error
        return ERR_LABEL_PHONE_NUMBER_CANNOT_BE_PARSED

    @staticmethod
    def get_valid_regions_for_phone_number(
        phone_str: str,
    ) -> dict[str, phonenumbers.PhoneNumber]:
        """
        Return a dictionary mapping region codes (ISO 3166) to parsed phone numbers.

        The returned dictionary only contain phone numbers that are valid for the
        country they are mapped from.

        :param phone_str: string containing a phone number.
        :return: dictionary mapping region codes (ISO 3166) to parsed phone numbers.
        """
        valid_phone_numbers = {}
        for region_code in phonenumbers.SUPPORTED_REGIONS:
            for match in phonenumbers.PhoneNumberMatcher(phone_str, region_code):
                number = match.number
                if phonenumbers.is_valid_number(
                    number
                ) and phonenumbers.is_valid_number_for_region(number, region_code):
                    number.raw_input = phone_str[match.start : match.end]
                    valid_phone_numbers[region_code] = number
                    break
        return valid_phone_numbers


def normalize_phone_number(phone_str: str) -> phonenumbers.PhoneNumber | str | None:
    """
    Normalize a phone number string, preferably to a E.164 format if it is valid.

    Correction priority:

    1. Auto infer region code + E.164 compliant + valid num values
    2. Provided region code + E.164 compliant + valid num values (order is important)
    3. NSN if string can be converted to int and has right number of digits
    4. None (nothing worked)

    This function uses the phonenumbers library's PhoneNumberMatcher to robustly
    find a phone number within a string, even if it's surrounded by other text
    or has varied formatting.

    If a default_region is not provided, it will iterate through a list of
    common regions to increase the chances of parsing a local number correctly.

    :param phone_str: The input string to search for a phone number.
    :return: The first valid phone number found, formatted as E.164 string, or None.
    """
    if not isinstance(phone_str, str):
        return None

    # Try with the `PhoneNumberMatcher` to search in messy strings and keep the matched
    # substring
    valid_phone_numbers = PhoneNumber.get_valid_regions_for_phone_number(phone_str)
    if len(valid_phone_numbers) > 0:
        return _get_most_likely_phone_number(valid_phone_numbers)

    # Nothing matched, so no way to have an E.164 compliant string or NSN that can be
    # valid with any region, return `None`
    return None


def _get_most_likely_phone_number(
    phone_numbers: dict[str, phonenumbers.PhoneNumber],
    # possible_country_codes: Collection[str] | None = None,
) -> phonenumbers.PhoneNumber | str:
    """Determine the most likely region code."""
    # Base case, there is only one possibility
    if len(phone_numbers) == 1:
        return next(iter(phone_numbers.values()))

    # Filter numbers by keeping the ones with the "raw_input" with the largest number of
    # digits (i.e. most complete parsed number)
    original_strings_digits = []  # excluding extensions
    for pn in phone_numbers.values():
        osd = "".join(re.findall(r"\+?\d+", pn.raw_input))
        if pn.extension is not None:
            osd = osd.rstrip(pn.extension)
        original_strings_digits.append(osd)
    max_num_digits_original_string = max([len(os) for os in original_strings_digits])
    phone_numbers_filtered = {
        rg: (pn, os)
        for (rg, pn), os in zip(phone_numbers.items(), original_strings_digits)
        if len(os) == max_num_digits_original_string
    }
    if len(phone_numbers_filtered) == 1:
        return next(iter(phone_numbers_filtered.values()))[0]

    # Try to see if one raw input matches exactly one local format
    phone_numbers_filtered_matched = {}
    for region, (phone_number, os) in phone_numbers_filtered.items():
        phone_number_national = phonenumbers.format_number(
            phone_number, phonenumbers.PhoneNumberFormat.NATIONAL
        )
        # If the national phone number format
        if phone_number.raw_input == phone_number_national:
            phone_numbers_filtered_matched[region] = (phone_number, os)
    if len(phone_numbers_filtered_matched) == 1:
        return next(iter(phone_numbers_filtered_matched.values()))[0]

    # Return most common original string digits
    os_count = Counter([os for (_, os) in phone_numbers_filtered.values()])
    max_count = max(count for count in os_count.values())
    os_count_filtered = {
        os: count for os, count in os_count.items() if count == max_count
    }

    # TODO more than one input string matched
    return next(iter(os_count_filtered))


r"""def _get_most_likely_phone_number_old(
    phone_numbers: dict[str, phonenumbers.PhoneNumber],
    # possible_country_codes: Collection[str] | None = None,
) -> phonenumbers.PhoneNumber | str:
    # Base case, there is only one possibility
    if len(phone_numbers) == 1:
        return next(iter(phone_numbers.values()))

    # Try to see if it matches a local format
    phone_numbers_filtered = {}
    # phone_numbers_national_formats = {}
    for region, phone_number in phone_numbers.items():
        phone_number_national = phonenumbers.format_number(
            phone_number, phonenumbers.PhoneNumberFormat.NATIONAL
        )
        # If the national phone number format
        if phone_number.raw_input == phone_number_national:
            phone_numbers_filtered[region] = phone_number
        # phone_numbers_national_formats[region] = phone_number_national
    if len(phone_numbers_filtered) == 1:
        return next(iter(phone_numbers_filtered.values()))
    elif len(phone_numbers_filtered) == 0:
        phone_numbers_filtered = phone_numbers

    # Rank phone number per levenshtein distance between the national format and the
    # original string matched. If there is one phone number with the lowest indel
    # distance, return this one.
    distances_international = [
        Levenshtein.distance(
            phone_number.raw_input,
            phonenumbers.format_number(
                phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
            ),
            weights=INDEL_WEIGHTS,
        )
        for phone_number in phone_numbers_filtered.values()
    ]
    # If any distance == 0: filter these out
    if min(distances_international) == 0:
        phone_numbers_filtered = {
            region: pn for (region, pn), distance in
            zip(phone_numbers.items(), distances_international)
            if distance == 0
        }
        if len(phone_numbers_filtered) == 1:
            return next(iter(phone_numbers_filtered.values()))
    # Filter per Levenshtein distance on the national format
    distances_national = [
        Levenshtein.distance(
            phone_number.raw_input,
            phonenumbers.format_number(
                phone_number, phonenumbers.PhoneNumberFormat.NATIONAL
            ),
            weights=INDEL_WEIGHTS,
        )
        for phone_number in phone_numbers_filtered.values()
    ]
    # If any distance == 0: filter these out
    if min(distances_national) == 0:
        phone_numbers_filtered = {
            region: pn for (region, pn), distance in
            zip(phone_numbers.items(), distances_national)
            if distance == 0
        }
        if len(phone_numbers_filtered) == 1:
            return next(iter(phone_numbers_filtered.values()))

    # Filter by keeping the ones with minimal edit distances (internat or nat)
    min_indel_distance = min(distances_international + distances_national)
    phone_numbers_filtered = {
        region: pn for (region, pn), dist_international, dist_national in
        zip(phone_numbers.items(), distances_international, distances_national)
        if (
            dist_international == min_indel_distance
            or dist_national == min_indel_distance
        )
    }
    if len(phone_numbers_filtered) == 1:
        return next(iter(phone_numbers_filtered.values()))

    # Multiple national formats with the same edit distance, filter them per length.
    # To return a full number safely, the difference between the edit distance of the
    # first and the second(s) should be significant
    # max_num_digits = max(nsns, key=lambda nsn: len(str(nsn)))
    max_num_digits_original = max(
        len(v.raw_input) for v in phone_numbers_filtered.values()
    )
    phone_numbers_filtered = {
        rg: v for rg, v in phone_numbers_filtered.items()
        if len(v.raw_input) == max_num_digits_original
    }
    if len(phone_numbers_filtered) == 1:
        return next(iter(phone_numbers_filtered.values()))

    # Multiple phone numbers matching the maximum number of digits in the original
    # text. Filter again by keeping the one with the highest number of digits in the
    # NSN.
    # not doing that, because a raw_string which is in fact a NSN can be parsed
    # as a full number for another country (if it begins with the same region code)
    '''max_num_digits_nsn = max(
        len(str(pn.national_number)) for pn in phone_numbers_filtered.values()
    )
    phone_numbers_filtered = {
        rg: pn for rg, pn in phone_numbers_filtered.items()
        if len(str(pn.national_number)) == max_num_digits_nsn
    }
    if len(phone_numbers_filtered) == 1:
        return next(iter(phone_numbers_filtered.values()))'''

    # At this point, the phone numbers have been filtered in all ways covered in this
    # method. We cannot deduce the country code and must return a NSN, and in particular
    # the digits as they appear in the original string input (i.e. including prefix
    # digits like "0" that are not part of the NSN).
    # Filter then per recurrence (keep the most recurrent one).
    nsn_count = Counter(
        [pn.national_number for pn in phone_numbers_filtered.values()]
    )
    max_count = max(count for count in nsn_count.values())
    nsn_count_filtered = {
        nsn: count for nsn, count in nsn_count.items() if count == max_count
    }

    # TODO More than one NSN which are the most common and having the maximum number of
    #  digits.
    nsn_target = next(iter(nsn_count_filtered))
    original_strings = [
        pn.raw_input for pn in phone_numbers_filtered.values()
        if pn.national_number == nsn_target
    ]
    # TODO more than one input string matched
    final_original_string = next(iter(original_strings))
    return "".join(re.findall('\d+', final_original_string))"""
