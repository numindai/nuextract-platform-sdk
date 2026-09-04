"""Language type."""

from __future__ import annotations

import importlib.resources
import re
from collections import defaultdict
from dataclasses import dataclass
from xml.etree import ElementTree as ET

from numind.nuextract_utils.data_validation.models import ErrorJson

from ._utils import AssociativeMapping, ClassCachedProperty
from .base import SemanticType
from .country import Country
from .language import Language
from .script import Script

ERR_LABEL_LANGUAGE_TAG_NOT_RFC_5646_COMPLIANT = (
    "label language code value is not ISO 639-3 compliant"
)
ERR_LABEL_LANGUAGE_RFC5646_COMPLIANT_BUT_CASE_INSENSITIVE = (
    "label language code/name value is ISO 639-3 compliant but only case-insensitive"
)


# Getting a mapping of scripts to languages from the IANA registry
GRANDFATHERED_TAGS, REDUNDANT_TAGS = [], []  # stored lowercase
with (
    importlib.resources.files("numind.nuextract_utils._iso_data")
    .joinpath("IANA language subtag registry.txt")
    .open(encoding="utf8") as _file
):
    raw_data = _file.read()
    primary = set()
    extlangs = set()
    script_to_langs = defaultdict(list)

    for record in raw_data.split("%%"):
        lines = record.strip().splitlines()
        if not lines:
            continue

        # collect the key → value pairs into a dict
        fields = {}
        for line in lines:
            if ": " in line:
                key_, value_ = line.split(": ", 1)
                fields[key_.strip()] = value_.strip()

        rtype = fields.get("Type")
        subtag_ = fields.get("Subtag")

        if rtype == "language":
            if subtag_:
                primary.add(subtag_)
            if "Suppress-Script" in fields:
                script_to_langs[fields["Suppress-Script"]].append(subtag_)
        elif rtype == "extlang" and subtag_:
            extlangs.add(subtag_)
        elif rtype == "grandfathered":
            GRANDFATHERED_TAGS.append(fields.get("Tag").lower())
        elif rtype == "redundant":
            REDUNDANT_TAGS.append(fields.get("Tag").lower())

    # freeze the two language sets so callers cannot mutate them
    PRIMARY_LANGUAGES = frozenset(primary)
    EXT_LANGUAGES = frozenset(extlangs)
# Using the CLDR likely subtags file to infer languages covered by each script
with (
    importlib.resources.files("numind.nuextract_utils._iso_data")
    .joinpath("CLDR likelySubtags.xml")
    .open("rb") as _file
):
    tree = ET.parse(_file)  # noqa: S314 - trusted bundled XML
    root = tree.getroot()

    # Find the <likelySubtags> element first (for robustness)
    likely_subtags = root.find("likelySubtags")

    for elem in likely_subtags.findall("likelySubtag"):
        from_tag = elem.attrib.get("from")
        to_tag = elem.attrib.get("to")
        # We're interested in entries where the 'to' has at least a script subtag
        parts_ = to_tag.split("_")
        if len(parts_) >= 2:
            lang_ = from_tag.split("_")[0]
            script_ = parts_[1]
            script_to_langs[script_].append(lang_)

SCRIPTS_TO_LANGUAGES = {k: frozenset(v) for k, v in script_to_langs.items()}
GRANDFATHERED_TAGS = frozenset(GRANDFATHERED_TAGS)
REDUNDANT_TAGS = frozenset(REDUNDANT_TAGS)


class Language2(Language):
    """Subclassing to change code subset without interfering with original type."""

    iso_subset_type = "codes_alpha2"


class LanguageTag(SemanticType):
    """
    Language tag following the IETF BCP 47 / RFC 5646 standard.

    A language tag identifies a language, optionally including its script, region, and
    variant. Its components must follow specific ISO or registry standards:

    - **Language subtag**: 2–3 letters (ISO 639-1/2) identifying the language, e.g.,
    "en" for English;
    - **Script subtag** (optional): 4 letters (ISO 15924) indicating the writing system,
    e.g., "Latn".
    - **Region subtag** (optional): 2 letters (ISO 3166-1) or 3 digits (UN M.49)
    specifying a country or region, e.g., "US".
    - **Variant subtags** (optional): 4–8 alphanumeric characters providing dialect,
    orthography, or other variations, e.g., "oxendict".
    - **Extensions and private-use subtags**: single-letter extensions and subtags for
    custom usage, e.g., "x-custom".

    :examples: `en-US` (English, United States), `zh-Hans-CN` (Simplified Chinese,
    China), `sl-rozaj` (Slovenian, Resian dialect)
    """  # noqa:RUF002

    json_schema_format = ("language-tag-IETF-BCP-47", "language-tag")
    # Class-level cached properties that auto-invalidate when source changes
    names_lower = ClassCachedProperty(
        "names", lambda s: {code.lower(): code for code in s}
    )
    language_data = AssociativeMapping("names", "codes_alphabetic")

    @classmethod
    def coerce(
        cls, value: str, input_text: str | None = None, error: ErrorJson | None = None
    ) -> str | None:
        """
        Try to fix a language name or code.

        :param value: language name/code to fix.
        :param input_text: input text.
        :param error: error associated to the value to convert. This argument
            can help to convert the value by targeting to the appropriate methods
            (default: ``None``).
        :return: a string corresponding to an ISO 639-3 language name or code, if the
            provided value can be converted, otherwise ``None``.
        """
        _ = input_text
        _ = error
        if not isinstance(value, str):
            return None

        if (language_tag := parse_language_tag(value)) is not None:
            return str(language_tag)

        return None

    @classmethod
    def validate(cls, value: str, _: str | None = None) -> str | None:
        """
        Check that a string is not considered "null" (and thus should be ``None``).

        :param value: string value to assess.
        :param _: placeholder for input text.
        :return: error message if the value should be ``None``, otherwise ``None``.
        """
        try:
            _ = parse_language_tag(value, autofix=False)
            return None
        except (ValueError, TypeError):
            return ERR_LABEL_LANGUAGE_TAG_NOT_RFC_5646_COMPLIANT


@dataclass
class LanguageTagStructured:
    """Structured representation of a BCP 47 language tag."""

    language: str | None = None
    ext_language: list[str] = None  # up to three
    script: str | None = None
    region: str | None = None
    variant: list[str] = None
    extension: dict[str, list[str]] | None = None
    private_use: list[str] | None = None
    grandfathered: str | None = None

    def __post_init__(self) -> None:
        """Initialize empty lists and dicts if None."""
        if self.ext_language is None:
            self.ext_language = []
        if self.variant is None:
            self.variant = []
        if self.extension is None:
            self.extension = {}
        if self.private_use is None:
            self.private_use = []

    def __str__(self) -> str:
        """
        Return the canonical string representation of the language tag.

        Returns:
            str: The properly formatted BCP 47 language tag

        """
        # Handle grandfathered tags
        if self.grandfathered:
            return self.grandfathered

        # Handle pure private use tags
        if self.private_use and not self.language:
            return "x-" + "-".join(self.private_use)

        # Build the tag components in order
        parts = []

        # Language (required for non-private-use tags)
        if self.language:
            parts.append(self.language)

        # Extended language subtags
        if self.ext_language:
            parts.extend(self.ext_language)

        # Script
        if self.script:
            parts.append(self.script)

        # Region
        if self.region:
            parts.append(self.region)

        # Variants
        if self.variant:
            parts.extend(self.variant)

        # Extensions (sorted by singleton for consistency)
        if self.extension:
            for singleton in sorted(self.extension.keys()):
                parts.append(singleton)
                parts.extend(self.extension[singleton])

        # Private use
        if self.private_use:
            parts.append("x")
            parts.extend(self.private_use)

        return "-".join(parts)


def parse_language_tag(tag: str, autofix: bool = True) -> LanguageTagStructured:
    """
    Parse an IETF BCP 47 language tag into structured components.

    https://github.com/silnrsi/langtags/blob/master/doc/langtags.md

    :param tag: The language tag string (e.g., 'en-US', 'zh-Hans-CN', 'x-private')
    :param autofix: whether to automatically fix tags and subtags that can be.
        (default: ``True``)
    :return: LanguageTag: Structured representation of the language tag.
    :raise ValueError: If the tag format is invalid.
    :raise TypeError: If the tag type is not a string.
    """
    # Store original for error messages
    if not isinstance(tag, str):
        raise TypeError(_ := f"Language tag must be a string, got {type(tag).__name__}")

    original_tag = tag
    tag = tag.strip()

    if tag == "":
        raise ValueError(_ := "Language tag cannot be empty")

    # Replacing characters to hyphens
    if autofix:
        for char in ("_", " ", ";", ":", "/", ","):
            tag = tag.replace(char, "-")
        # Remove trailing hyphens
        while tag.endswith("-"):
            tag = tag[:-1]
        # Deduplicating consecutive hyphens
        while "--" in tag:
            tag = tag.replace("--", "-")

    # Check for invalid characters
    if not re.match(r"^[a-zA-Z0-9\-]+$", tag):
        raise ValueError(
            _ := f"Language tag contains invalid characters: '{original_tag}'"
        )
    # Check for invalid hyphen patterns
    if tag.startswith("-") or tag.endswith("-"):
        raise ValueError(
            _ := f"Language tag cannot start or end with hyphen: '{original_tag}'"
        )
    if "--" in tag:
        raise ValueError(
            _ := f"Language tag cannot contain consecutive hyphens: '{original_tag}'"
        )

    if tag.lower() in GRANDFATHERED_TAGS:
        return LanguageTagStructured(grandfathered=tag.lower())

    # Split into subtags
    subtags = tag.split("-")

    # Check for empty subtags
    for i, subtag in enumerate(subtags):
        if not subtag:
            raise ValueError(_ := f"Empty subtag at position {i} in: '{original_tag}'")

    result = LanguageTagStructured()
    i = 0

    # Handle private use tags (starting with 'x')
    if subtags[0].lower() == "x":
        if len(subtags) < 2:
            raise ValueError(
                _ := "Private use tag must have at least one subtag after 'x'"
            )
        result.private_use = [s.lower() for s in subtags[1:]]
        return result

    # Parse language subtag (2-3 or 5-8 characters, letters only)
    if i < len(subtags):
        lang = subtags[i]
        if re.match(r"^[a-zA-Z]{2,3}$", lang) or re.match(r"^[a-zA-Z]{5,8}$", lang):
            if (lang_err := Language2.validate(lang)) is not None:
                lang_err = ErrorJson([], error_message=lang_err)
                if (
                    autofix
                    and (lang_code := Language2(lang, error=lang_err)) is not None
                ):
                    lang = lang_code
                else:
                    raise ValueError(_ := f"Language subtag is invalid ({lang})")
            result.language = lang
            i += 1
        else:
            # Provide specific error messages for common mistakes
            if lang.isdigit():
                raise ValueError(
                    _ := f"Language tag cannot start with a number: '{original_tag}'"
                )
            if len(lang) == 1:
                raise ValueError(
                    _ := f"Language subtag must be 2-3 or 5-8 letters, got single "
                    f"character: '{lang}' in '{original_tag}'"
                )
            if len(lang) == 4 and re.match(r"^[a-zA-Z]{4}$", lang):
                raise ValueError(
                    _ := f"4-letter subtag '{lang}' appears to be a script code but "
                    f"no language specified in: '{original_tag}'"
                )
            if not re.match(r"^[a-zA-Z]+$", lang):
                raise ValueError(
                    _ := f"Language subtag must contain only letters: '{lang}' in "
                    f"'{original_tag}'"
                )
            raise ValueError(
                _ := f"Invalid language subtag length ({len(lang)} characters): "
                f"'{lang}' in '{original_tag}'"
            )

    # Parse extlang subtags (3 letters, up to 3 allowed)
    extlang_count = 0
    while i < len(subtags) and extlang_count < 3:
        if re.match(r"^[a-zA-Z]{3}$", subtags[i]):
            if (lang_err := Language.validate(subtags[i])) is not None:
                lang_err = ErrorJson([], error_message=lang_err)
                if (
                    autofix
                    and (lang_code := Language(subtags[i].lower(), error=lang_err))
                    is not None
                    and lang_code in EXT_LANGUAGES
                ):
                    subtags[i] = lang_code
                else:
                    raise ValueError(_ := f"Language subtag is invalid ({subtags[i]})")
            result.ext_language.append(subtags[i])
            extlang_count += 1
            i += 1
        else:
            break

    # Parse script subtag (4 letters)
    if i < len(subtags) and re.match(r"^[a-zA-Z]{4}$", subtags[i]):
        if Script.validate(subtags[i]) is not None:
            # check that there is at least one language covered by the script
            if (
                autofix
                and (script := Script(subtags[i].capitalize())) is not None
                and result.language in SCRIPTS_TO_LANGUAGES[script]
            ):
                subtags[i] = script
            else:
                raise ValueError(_ := f"Script subtag is invalid ({subtags[i]})")
        result.script = subtags[i]
        i += 1

    # Parse region subtag (2 letters or 3 digits)
    if i < len(subtags):
        region = subtags[i]
        if re.match(r"^[a-zA-Z]{2}$", region):
            country_code_err = Country.validate(region)
            if country_code_err is not None:
                country_code_err = ErrorJson([], Country.validate(region))
                if (
                    autofix
                    and (
                        region_fixed := Country(region.upper(), error=country_code_err)
                    )
                    is not None
                ):
                    subtags[i] = region_fixed
                else:
                    raise ValueError(_ := f"Region code is invalid ({subtags[i]})")
            result.region = subtags[i]
            i += 1
        elif re.match(r"^[0-9]{3}$", region):  # UN M.49
            result.region = region
            i += 1

    # Parse variant subtags (5-8 alphanum OR 4 chars starting with digit)
    while i < len(subtags):
        variant = subtags[i]
        if re.match(r"^[a-zA-Z0-9]{5,8}$", variant) or re.match(
            r"^[0-9][a-zA-Z0-9]{3}$", variant
        ):
            # Check if it's actually an extension singleton
            if len(variant) == 1 and re.match(r"^[a-zA-Z0-9]$", variant):
                break
            result.variant.append(variant.lower())
            i += 1
        else:
            # Check if this might be an extension
            if len(variant) == 1 and re.match(r"^[a-zA-Z0-9]$", variant):
                break
            # Provide specific error for invalid variants
            if not re.match(r"^[a-zA-Z0-9]+$", variant):
                raise ValueError(
                    _ := f"Invalid variant subtag contains non-alphanumeric characters"
                    f": '{variant}' in '{original_tag}'"
                )
            if len(variant) < 4:
                raise ValueError(
                    _ := f"Variant subtag too short (minimum 4 characters): "
                    f"'{variant}' in '{original_tag}'"
                )
            if len(variant) > 8:
                raise ValueError(
                    _ := f"Variant subtag too long (maximum 8 characters): '{variant}' "
                    f"in '{original_tag}'"
                )
            raise ValueError(
                _ := f"Invalid variant subtag format: '{variant}' in '{original_tag}'"
            )

    # Parse extensions and private use
    while i < len(subtags):
        if i + 1 >= len(subtags):
            # Lone subtag at end
            raise ValueError(
                _ := f"Unexpected subtag at end: '{subtags[i]}' in '{original_tag}'"
            )

        singleton = subtags[i]

        # Private use extension
        if singleton.lower() == "x":
            result.private_use = [s.lower() for s in subtags[i + 1 :]]
            break

        # Regular extension
        if (
            len(singleton) == 1
            and re.match(r"^[a-zA-Z0-9]$", singleton)
            and singleton.lower() != "x"
        ):
            singleton = singleton.lower()
            i += 1
            ext_subtags = []

            # Collect extension subtags (2-8 alphanum)
            while i < len(subtags):
                subtag = subtags[i]
                if re.match(r"^[a-zA-Z0-9]{2,8}$", subtag):
                    ext_subtags.append(subtag.lower())
                    i += 1
                else:
                    break

            if ext_subtags:
                result.extension[singleton] = ext_subtags
            else:
                raise ValueError(
                    _ := f"Extension '{singleton}' must have at least one subtag in "
                    f"'{original_tag}'"
                )
        else:
            # Invalid remaining subtag
            if len(singleton) > 1:
                raise ValueError(
                    _ := f"Unexpected subtag (not a valid extension or private use): "
                    f"'{singleton}' in '{original_tag}'"
                )
            raise ValueError(
                _ := "Invalid extension singleton: '{singleton}' in '{original_tag}'"
            )

    # Final validation
    # Invalid language tag - must have at least a language subtag or be a private use
    # tag: '{original_tag}'
    if not result.language and not result.private_use and not result.grandfathered:
        raise ValueError(
            _ := f"Invalid language tag - must have at least a language subtag or be a "
            f"private use tag: '{original_tag}'"
        )

    return result
