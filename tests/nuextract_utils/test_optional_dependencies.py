"""Tests for NuExtract validation without optional dependencies."""

from __future__ import annotations

import subprocess
import sys

import pytest


def test_validation_falls_back_without_optional_dependencies() -> None:
    """Check that validation imports and basic fallbacks work without the extra."""
    fallback_script = r'''
import importlib.abc
import sys

blocked_dependencies = {
    "cdifflib",
    "emval",
    "phonenumbers",
    "rapidfuzz",
    "regex",
    "schwifty",
    "stringzilla",
    "sympy",
}


class BlockOptionalDependencies(importlib.abc.MetaPathFinder):
    """Prevent optional dependencies from being imported in this subprocess."""

    def find_spec(self, fullname, path=None, target=None):
        if fullname.partition(".")[0] in blocked_dependencies:
            raise ModuleNotFoundError(
                f"blocked optional dependency: {fullname}", name=fullname
            )
        return None


sys.meta_path.insert(0, BlockOptionalDependencies())

from numind.nuextract_utils.data_validation.data_correction import (
    correct_input_template,
)
from numind.nuextract_utils.data_validation.types.bic import BIC
from numind.nuextract_utils.data_validation.types.email_address import EmailAddress
from numind.nuextract_utils.data_validation.types.iban import IBAN
from numind.nuextract_utils.data_validation.types.integer import Integer
from numind.nuextract_utils.data_validation.types.number import Number
from numind.nuextract_utils.data_validation.types.phone_number import PhoneNumber
from numind.nuextract_utils.data_validation.types.rfc3987 import match, parse
from numind.nuextract_utils.data_validation.types.verbatim_string import (
    find_closest_verbatim_string,
    is_verbatim_string_valid,
    smart_tokenize,
)

assert EmailAddress.validate("not an email") is None
assert EmailAddress.coerce("user at example dot com") == "user at example dot com"
assert BIC.validate("not a BIC") is None
assert IBAN.validate("not an IBAN") is None
assert PhoneNumber.validate("not a phone") is None
assert EmailAddress.validate(123) is not None
assert BIC.validate(123) is not None
assert IBAN.validate(123) is not None
assert PhoneNumber.validate(123) is not None
assert Number.coerce("1,5") == 1.5
assert Number.coerce("1/2") is None
assert Integer.coerce("2+2") is None
assert match("https://例子.测试/路径", "IRI")
assert parse("https://例子.测试/路径", "IRI")["authority"] == "例子.测试"
assert smart_tokenize("中文 test") == ["中文", "test"]
assert is_verbatim_string_valid("中文", "some 中文 text") is None
assert find_closest_verbatim_string("hello world", "hello word") == ""

corrected_template, _ = correct_input_template({"value": "strng"})
assert corrected_template == {}
'''

    subprocess.run(  # noqa: S603 - executes a static test script with this interpreter
        [sys.executable, "-c", fallback_script],
        check=True,
        text=True,
        capture_output=True,
    )


def test_cdifflib_falls_back_to_difflib() -> None:
    """Keep fuzzy correction working when only its accelerator is unavailable."""
    fallback_script = r'''
import importlib.abc
import sys


class BlockCdifflib(importlib.abc.MetaPathFinder):
    """Prevent cdifflib from being imported in this subprocess."""

    def find_spec(self, fullname, path=None, target=None):
        if fullname.partition(".")[0] == "cdifflib":
            raise ModuleNotFoundError("blocked optional dependency: cdifflib")
        return None


sys.meta_path.insert(0, BlockCdifflib())

from numind.nuextract_utils.data_validation.types.verbatim_string import (
    find_closest_verbatim_string,
)

assert find_closest_verbatim_string("hello world", "hello word") == "hello world"
'''

    subprocess.run(  # noqa: S603 - executes a static test script with this interpreter
        [sys.executable, "-c", fallback_script],
        check=True,
        text=True,
        capture_output=True,
    )


def test_regex_supports_mixed_unicode_scripts() -> None:
    """Preserve advanced Unicode tokenization when regex is installed."""
    pytest.importorskip("regex")

    from numind.nuextract_utils.data_validation.types.rfc3987 import match
    from numind.nuextract_utils.data_validation.types.verbatim_string import (
        smart_tokenize,
    )

    assert match("https://例子.测试/路径", "IRI")
    assert smart_tokenize("中文ひらがな test") == ["中文", "ひらがな", "test"]
