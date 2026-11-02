"""Country subdivision types."""

from __future__ import annotations

import csv
import importlib.resources
from typing import TYPE_CHECKING, Literal

from ._utils import ClassCachedProperty, MappingInterface
from .base import SemanticType

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson

ERR_LABEL_REGION_NOT_ISO_3166_COMPLIANT = (
    "label region code/name value is not ISO 3166 compliant"
)
ERR_LABEL_REGION_ISO_3166_COMPLIANT_BUT_CASE_INSENSITIVE = (
    "label region code/name value is ISO 3166 compliant but only case-insensitive"
)
SUPPORTED_COUNTRIES = (
    "US",
    "FR",
    "IE",
    "GB",
    "IT",
    "ES",
    "DE",
    "PT",
    "CA",
    "MX",
    "BR",
    "AU",
    "JP",
    "KR",
    "CN",
    "IN",
    "VN",
    "TH",
    "RU",
    "PL",
)
_EXAMPLES = {
    "US": (
        "`US-NY` (New York state), `US-DC` (District of Columbia), "
        "`US-GU` (Guam outlying area)"
    ),
    "FR": (
        "`FR-49` (Maine-et-Loire département), `FR-MQ` (Martinique overseas region), "
        "`FR-V` (Rhône-Alpes région)."
    ),
    "IE": (
        "`IE-D` (Dublin county), `IE-C` (Connacht province), `IE-WD` (Waterford county)"
    ),
    "GB": (
        "`GB-WSX` (West Sussex two-tier county), `GB-WSM` (Westminster borough), "
        "`GB-WIL` (Wiltshire unitary authority)"
    ),
    "IT": (
        "`IT-RM` (Rome province), `IT-BZ` (Bolzano province), `IT-82` (Sicily region)"
    ),
    "ES": (
        "`ES-GA` (Galicia autonomous community), `ES-GR` (Granada province), "
        "`ES-ML` (Melilla autonomous city)"
    ),
    "DE": "`DE-BY` (Bayern state), `DE-BE` (Berlin state), `DE-HH` (Hamburg state)",
    "PT": "`PT-11` (Lisbon district), `PT-20` (Azores autonomous region)",
    "CA": (
        "`CA-QC` (Quebec province), `CA-NU` (Nunavut territory), "
        "`CA-YT` (Yukon territory)"
    ),
    "MX": (
        "`MX-JAL` (Jalisco state), `MX-DIF` (Distrito Federal), "
        "`MX-AGU` (Aguascalientes state)"
    ),
    "BR": (
        "`BR-RJ` (Rio de Janeiro state), `BR-DF` (Distrito Federal), "
        "`BR-SP` (São Paulo state)"
    ),
    "AU": (
        "`AU-NSW` (New South Wales state), `AU-VIC` (Victoria state), "
        "`AU-ACT` (Australian Capital Territory)"
    ),
    "JP": (
        "`JP-13` (Tokyo metropolis), `JP-27` (Osaka urban prefecture), "
        "`JP-01` (Hokkaidō territory)"
    ),
    "KR": (
        "`KR-11` (Seoul capital metropolitan city), `KR-26` (Busan metropolitan city), "
        "`KR-41` (Gyeonggi-do province)"
    ),
    "CN": (
        "`CN-11` (Beijing municipality), `CN-44` (Guangdong province), "
        "`CN-65` (Xinjiang autonomous region)"
    ),
    "IN": (
        "`IN-MH` (Maharashtra state), `IN-DL` (Delhi union territory), "
        "`IN-JK` (Jammu and Kashmir state)"
    ),
    "VN": (
        "`VN-HN` (Hanoi municipality), `VN-SG` (Ho Chi Minh City municipality), "
        "`VN-31` (Binh Dinh province)"
    ),
    "TH": (
        "`TH-10` (Krung Thep Maha Nakhon / Bangkok), `TH-50` (Chiang Mai province), "
        "`TH-82` (Phang Nga province)"
    ),
    "RU": (
        "`RU-SPE` (Saint Petersburg autonomous city), `RU-MOS` (Moskovskaya oblast), "
        "`RU-TA` (Tatarstan republic)"
    ),
    "PL": (
        "`PL-MA` (Lesser Poland / Małopolskie voivodeship), `PL-DS` (Lower Silesia / "
        "Dolnośląskie voivodeship), `PL-PM` (Pomeranian / Pomorskie voivodeship)"
    ),
}

COUNTRY_TO_REGIONS = {}
with (
    importlib.resources.files("numind.nuextract_utils._iso_data")
    .joinpath("ISO 3166-2.csv")
    .open(encoding="utf8") as _file
):
    reader_ = csv.reader(_file, delimiter=";")
    next(reader_)
    for row in reader_:
        if (region_code := row[0]) not in COUNTRY_TO_REGIONS:
            COUNTRY_TO_REGIONS[region_code] = {
                "names": [],
                "types": [],
                "codes_alpha3": [],
            }

        COUNTRY_TO_REGIONS[region_code]["names"].append(row[1])
        COUNTRY_TO_REGIONS[region_code]["types"].append(row[2].lower())
        COUNTRY_TO_REGIONS[region_code]["codes_alpha3"].append(
            f"{region_code}-{row[3].strip()}"
        )


# This class is intended to be subclassed by country-level classes handling its
# associated subdivisions (regions).
class Region(SemanticType):
    """
    Uppercase subdivision code complying to ISO 3166-2:<COUNTRY>.

    <COUNTRY> is the ISO 3166-1 alpha-2 code of the corresponding country.

    :examples:
    """

    json_schema_format = "region-code-ISO_3166-2:<COUNTRY>"
    country_code: str
    iso_subset_type: Literal["names", "codes_alpha3"] = "codes_alpha3"
    # dictionaries to be used as ordered sets to build `country_data`
    # Subdivision codes include the uppercase 2-character country code and hyphen.
    mapping: MappingInterface = None
    names: set[str] = ClassCachedProperty(
        "mapping",
        lambda m: {
            g[m.group_names["names"]]
            for g in m._groups
            if g[m.group_names["names"]] is not None
        },
        "_names_cached",
    )  # Title case
    types: set[str] = ClassCachedProperty(
        "mapping",
        lambda m: {
            g[m.group_names["types"]]
            for g in m._groups
            if g[m.group_names["types"]] is not None
        },
        "_types_cached",
    )  # Title case
    codes_alpha3: set[str] = ClassCachedProperty(
        "mapping",
        lambda m: {g[m.group_names["codes_alpha3"]] for g in m._groups},
        "_codes_alpha3_cached",
    )  # uppercase

    # Class-level cached properties that auto-invalidate when source changes
    names_lower = ClassCachedProperty(
        "names", lambda s: {code.lower(): code for code in s}, "_names_lower_cached"
    )
    codes_alpha3_lower = ClassCachedProperty(
        "codes_alpha3",
        lambda s: {code.lower(): code for code in s},
        "_codes_alpha3_lower_cached",
    )

    @classmethod
    def coerce(
        cls, value: str, input_text: str | None = None, error: ErrorJson | None = None
    ) -> str | None:
        """
        Try to fix a region name or code.

        :param value: subdivision name or code, with or without the country prefix.
        :param input_text: input text.
        :param error: error associated to the value to convert. This argument
            can help to convert the value by targeting to the appropriate methods
            (default: ``None``).
        :return: an ISO 3166-2 subdivision name or prefixed code if the value can
            be converted, otherwise ``None``.
        """
        _ = input_text
        if not isinstance(value, str):
            return None

        # Correct case unsensitive errors
        if (
            error is not None
            and error.error_message
            == ERR_LABEL_REGION_ISO_3166_COMPLIANT_BUT_CASE_INSENSITIVE
            and cls.iso_subset_type == "codes_alpha3"
        ):
            return value.upper()

        # Try to correct based on groups
        group = cls.mapping.get_group(value.lower())
        if group is None:
            group = cls.mapping.get_group(f"{cls.country_code}-{value}".lower())
        if group is not None:
            idx_to_get = cls.mapping.group_names[cls.iso_subset_type]
            return group[idx_to_get]

        return None

    @classmethod
    def validate(cls, value: str, _: str | None = None) -> str | None:
        """
        Check a subdivision value against this country's ISO 3166-2 data.

        :param value: string value to assess.
        :param _: placeholder for input text.
        :return: error message for an invalid value or casing, otherwise ``None``.
        """
        valid_case_sensitive = value in cls._get_valid_set()
        if not valid_case_sensitive:
            if value.lower() in cls._get_valid_set_lowercase():
                return ERR_LABEL_REGION_ISO_3166_COMPLIANT_BUT_CASE_INSENSITIVE
            return ERR_LABEL_REGION_NOT_ISO_3166_COMPLIANT
        return None

    @classmethod
    def _get_valid_set(cls) -> set[str]:
        if cls.iso_subset_type == "codes_alpha3":
            return cls.codes_alpha3
        return cls.names

    @classmethod
    def _get_valid_set_lowercase(cls) -> set[str]:
        if cls.iso_subset_type == "codes_alpha3":
            return cls.codes_alpha3_lower
        return cls.names_lower


# Dynamically creating Region classes for each country
REGIONS_TYPES = {}
for country_code in SUPPORTED_COUNTRIES:
    regions_info = COUNTRY_TO_REGIONS[country_code]
    # build the attribute dict; using a regular assignment, not an annotation
    regions_mapping = MappingInterface.from_data(**regions_info)
    attrs = {
        "mapping": regions_mapping,
        "country_code": country_code,
        "__qualname__": (cls_name := f"Region{country_code}"),  # for repr/help()
    }
    # create the subclass:  type(name, bases, attrs)
    region_cls = type(cls_name, (Region,), attrs)
    region_cls.__doc__ = Region.__doc__.replace("<COUNTRY>", country_code)
    region_cls.json_schema_format = region_cls.json_schema_format.replace(
        "<COUNTRY>", country_code
    )
    if country_code in _EXAMPLES:
        region_cls.__doc__ = region_cls.__doc__.replace(
            ":examples:", f":examples: {_EXAMPLES[country_code]}"
        )

    REGIONS_TYPES[f"region:{country_code}"] = region_cls

COMMON_REGION_DOCS = (
    'Uppercase subdivision code complying to ISO 3166-2, where "XX" is an '
    "'uppercase 2-characters ISO 3166-1 country code among: "
    f'{", ".join(SUPPORTED_COUNTRIES)}. For example for region:US: "US-NY" for the '
    f'state of New York, "US-DC" for the District of Columbia district, or "US-GU" '
    f'for the Guam outlying area. For example for region:FR: "FR-49" for the '
    f'"Maine-et-Loire" département, or "FR-MQ" for the Martinique oversea region, '
    f'or "FR-V" for the "Rhône-Alpes" région.'
)
