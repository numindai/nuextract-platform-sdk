"""Email address type."""

from __future__ import annotations

import re
import unicodedata
from typing import TYPE_CHECKING

from emval import EmailValidator

from .base import SemanticType

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson

ERR_LABEL_EMAIL_ADDRESS_IS_MALFORMED = (
    "label leaf email address value is not RFC 3987 compliant"
)

EMAIL_VALIDATOR = EmailValidator(
    allow_smtputf8=True,
    allow_empty_local=False,
    allow_quoted_local=False,
    allow_domain_literal=True,
    deliverable_address=False,
)
CHAR_FIXES = {
    " at ": "@",
    " dot ": ".",
    "(at)": "@",
    "(dot)": ".",
    "[at]": "@",
    "[dot]": ".",
    # Unicode variations
    "＠": "@",  # Fullwidth at sign
    "。": ".",  # Ideographic full stop
    "．": ".",  # Fullwidth full stop
    "·": ".",  # Middle dot
    "･": ".",  # Halfwidth katakana middle dot
}


class EmailAddress(SemanticType):
    """
    An email address string complying the RFC 5322 and RFC 6531 standards.

    It is composed of a local part (username), the "@" separator, and a domain name.
    The local part may include dots, hyphens, underscores, or quoted strings, while the
    domain follows DNS naming rules and may include internationalized characters.

    :examples: `firstname.lastname@example.com`, `用户@例子.公司`
    """

    # idn-email is RFC 6531 which includes RFC 5322
    json_schema_format = ("idn-email", "email", "email-address")
    email_validator: EmailValidator = EMAIL_VALIDATOR

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
        _ = error
        if not isinstance(value, str):
            return str(value)

        # Try to correct string to an email
        email_fixed = cls.fix_malformed_email_address(value)
        # Make sure it is actually rfc compliant
        if email_fixed is not None and cls.validate(email_fixed) is None:
            return email_fixed
        # Couldn't be fixed
        return None

    @classmethod
    def fix_malformed_email_address(cls, email: str) -> str | None:
        """
        Attempt to fix common email address malformations.

        While preserving Unicode characters.

        :param email: The potentially malformed email address.
        :return: Corrected email address if fixable, None if unfixable.
        """
        if not email or not isinstance(email, str):
            return None

        # Strip whitespace (Unicode-aware)
        email = email.strip()

        if not email:
            return None

        # Fix common character replacements (including Unicode variants)
        for wrong, correct in CHAR_FIXES.items():
            email = email.replace(wrong, correct)

        # Remove extra spaces that may have been created by replacements
        email = re.sub(r"\s+", " ", email)
        email = email.strip()

        # Remove spaces around @ symbol
        email = re.sub(r"\s*@\s*", "@", email)

        # Remove multiple consecutive dots
        email = re.sub(r"\.{2,}", ".", email)

        # Fix consecutive @ symbols
        while "@@" in email:
            email = email.replace("@@", "@")

        # If multiple @ symbols remain, return None
        if email.count("@") != 1:
            return None

        # Split into local and domain parts
        local_part, domain_part = email.split("@")

        # Clean up local part
        local_part = local_part.strip().strip(".")

        # Clean up domain part - remove spaces but be strict about trailing dots
        domain_part = domain_part.strip()
        # Remove all spaces from domain
        domain_part = re.sub(r"\s+", "", domain_part)

        # If domain ends with a dot, it's likely malformed for email (FQDN not
        # appropriate)
        if domain_part.endswith("."):
            return None

        if not local_part or not domain_part:
            return None

        # Apply Unicode normalization
        email = unicodedata.normalize("NFC", f"{local_part}@{domain_part}")

        # Split again after normalization if needed
        local_part, domain_part = email.split("@")

        # Apply RFC-compliant case handling: local part case-sensitive, domain
        # case-insensitive
        # Domain part: convert all characters to lowercase using casefold for proper
        # Unicode handling
        domain_part = domain_part.casefold()

        email = f"{local_part}@{domain_part}"

        # Basic validation - must have proper structure
        if not re.match(r"^.+@.+$", email):
            return None

        # Validate local and domain parts separately
        local_part, domain_part = email.split("@")

        # Local part: allow Unicode word chars, dots, plus, percent, hyphen
        # The emval validator is quite strict on local part, so this regex should align
        # with what emval generally accepts or at least not be too permissive.
        # For simplicity and to avoid re-implementing emval's strictness,
        # we'll keep a general check here, but the ultimate validation is
        # `cls.email_validator.validate_email`.
        if not re.match(r"^[\w.!#$%&\'*+/=?^_`{|}~-]+$", local_part, re.UNICODE):
            # Relaxed a bit based on common local part chars. emval is the ultimate gate
            pass

        # Domain part: allow Unicode word chars, dots, hyphens (must have at least one
        # dot for TLD)
        # Note: IDN domains can be single-label, but typically we expect a TLD.
        # emval will handle IDN specific rules.
        if not re.match(r"^[\w-]+(?:\.[\w-]+)+$", domain_part, re.UNICODE):
            # Allow single word domains for special cases like 'localhost', but these
            # often aren't deliverable addresses and `emval` might flag them unless
            # configured. We'll rely on emval for the strict validation.
            pass

        return email

    @classmethod
    def validate(cls, value: str, _: str | None = None) -> str | None:
        """
        Check that a string is indeed a valid email address.

        :param value: string value to assess.
        :param _: placeholder for text_input.
        :return: error message if the value is not valid, otherwise ``None``.
        """
        if not isinstance(value, str):
            return ERR_LABEL_EMAIL_ADDRESS_IS_MALFORMED  # Or handle as per your design

        # RFC 5321 and 5322 state that the domain part is case-insensitive.
        # For validation, we should ensure it is indeed lowercase or consider it
        # malformed
        # if the fixing logic should enforce it.
        # The fix_malformed_email_address should already lowercase it,
        # but as a final check before emval, let's ensure this.
        if "@" in value:
            _, domain_part = value.split("@", 1)
            # Check if domain part contains any uppercase ASCII characters
            if any(c.isupper() for c in domain_part if "A" <= c <= "Z"):
                return ERR_LABEL_EMAIL_ADDRESS_IS_MALFORMED

        try:
            _ = cls.email_validator.validate_email(value)
        except (ValueError, SyntaxError):
            return ERR_LABEL_EMAIL_ADDRESS_IS_MALFORMED

        return None
