"""
URL type.

It is in fact IRI (Uniform Resource Identifier), i.e.  URI (URL with queries and
fragments) where Unicode (non-ascii) characters are allowed.
"""

from __future__ import annotations

import re
import urllib.parse
from typing import TYPE_CHECKING

from .base import SemanticType
from .rfc3987 import match

if TYPE_CHECKING:
    from numind.nuextract_utils.data_validation.models import ErrorJson

ERR_LABEL_URL_IS_MALFORMED = "label leaf URL (IRI) value is not RFC 3987 compliant"

DEFAULT_HTTP_SCHEME = "https"


"""# Loading existing TLDs
try:
    tlds = requests.get("https://data.iana.org/TLD/tlds-alpha-by-domain.txt").text
except requests.exceptions.RequestException:
    with (
        importlib.resources.files("numind.nuextract_utils._iso_data")
                .joinpath("IANA tlds.txt")
                .open(encoding="utf8") as _file
    ):
        tlds = _file.read()
TLDS = []
for line in tlds.splitlines()[1:]:  # skipping first line
    TLDS.append(line := line.strip().lower())
    if line.startswith("xn--"):  # storing Unicode versions too
        TLDS.append(line.encode("ascii").decode('idna'))"""


class URL(SemanticType):
    """
    An IRI (Internationalized Resource Identifier) following the RFC 3987 standard.

    An IRI extends the URI syntax defined in RFC 3986 by allowing Unicode characters
    beyond the ASCII set. It can identify resources using schemes such as HTTP, HTTPS,
    FTP, or mailto. When IRIs are transmitted in protocols that require ASCII-only
    encoding, they are converted to URIs through percent-encoding and Punycode (for
    internationalized domain names, per IDNA2008).

    Components:
    - **Scheme**: protocol identifier, e.g., "http", "https", "ftp".
    - **Authority**: includes user info, host, and port. Hosts may be internationalized
      domain names (IDN, RFC 5890+) using Unicode.
    - **Path**: hierarchical part of the resource, may include Unicode characters.
    - **Query**: additional data, introduced by "?", may include Unicode.
    - **Fragment**: identifier within the resource, introduced by "#".

    :examples: `http://www.example.com/` (HTTP URL with ASCII-only host and no
    path/query/fragment), `https://例子.测试/路径?查询=值#片段` (HTTPS IRI with an
    internationalized domain name, Unicode path, query, and fragment),
    `ftp://user:password@host.example/文件.txt` (An FTP IRI with user credentials, ASCII
    host, and a Unicode filename)
    """

    json_schema_format = ("iri", "uri", "url")

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

        # Try to correct string to a url
        url_fixed = cls.fix_malformed_url(value)
        # Make sure it is actually rfc compliant
        if url_fixed is not None and cls.validate(url_fixed) is None:
            return url_fixed
        # Couldn't be fixed
        return None

    @classmethod
    def fix_malformed_url(cls, url: str) -> str | None:
        """
        Attempt to fix common URL malformations.

        :param url: The potentially malformed URL.
        :return: The corrected URL if fixable, None if unfixable
        """
        if not url or not isinstance(url, str):
            return None

        # Strip whitespace
        url = url.strip()

        # Check for empty or whitespace-only strings
        if not url:
            return None

        # Check for obviously invalid cases
        if url in [".", "..", "...", "http://", "https://", "http://.", "https://."]:
            return None

        # Handle specific case
        if url.lower() == "localhost":
            return f"{DEFAULT_HTTP_SCHEME}://{url.lower()}"

        # Check for text that doesn't look like a URL at all
        if not re.search(r"[.\-:]", url) and not url.startswith(
            ("http://", "https://", "ftp://", "mailto:", "file://")
        ):
            return None

        # Handle non-HTTP protocols - return as-is if they're already valid schemes
        # But exclude cases where it's just a hostname with port e.g., example.com:8080
        # Check if it's a hostname:port pattern rather than a protocol
        if (
            re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", url)
            and not re.match(r"^https?://", url, re.IGNORECASE)
            and not url.startswith(("://", "//"))
            and not re.match(r"^[a-zA-Z0-9.-]+:\d+", url)
        ):
            return url

        # Handle malformed schemes
        if url.startswith("://"):
            url = DEFAULT_HTTP_SCHEME + url
        elif url.startswith("//"):
            url = DEFAULT_HTTP_SCHEME + ":" + url

        # Handle cases like "http.example.com" or "https.example.com"
        if re.match(r"^(https?)\.([\w.-]+)", url, re.IGNORECASE):
            match = re.match(r"^(https?)\.([\w.-]+.*)", url, re.IGNORECASE)
            if match:
                scheme, rest = match.groups()
                url = f"{scheme.lower()}://{scheme.lower()}.{rest}"

        # Add scheme if missing (but not for hostname:port patterns)
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", url) or re.match(
            r"^[a-zA-Z0-9.-]+:\d+", url
        ):
            url = DEFAULT_HTTP_SCHEME + "://" + url

        # Parse the URL
        try:
            parsed = urllib.parse.urlparse(url)
            # Normalize scheme to lowercase
            if parsed.scheme:
                parsed = parsed._replace(scheme=parsed.scheme.lower())
        except (TypeError, UnicodeDecodeError, ValueError):
            return None

        # Fix malformed netloc (e.g., "http:///example.com" -> "http://example.com")
        if parsed.scheme and not parsed.netloc and parsed.path:
            # Check if the path starts with what should be a netloc
            path_parts = parsed.path.lstrip("/").split("/", 1)
            if path_parts[0] and "." in path_parts[0]:
                new_netloc = path_parts[0]
                new_path = "/" + path_parts[1] if len(path_parts) > 1 else ""
                parsed = parsed._replace(netloc=new_netloc, path=new_path)

        # Clean up netloc - remove extra dots and normalize case
        if parsed.netloc:
            # Remove internal whitespace
            netloc = re.sub(r"\s+", "", parsed.netloc)
            # Fix multiple consecutive dots
            netloc = re.sub(r"\.{2,}", ".", netloc)
            # Convert to lowercase (domain names are case-insensitive)
            netloc = netloc.lower()
            parsed = parsed._replace(netloc=netloc)

        # Remove trailing slash from path if it's just "/"
        if parsed.path == "/":
            parsed = parsed._replace(path="")
        # Remove trailing slash from paths that end with "/"
        elif parsed.path.endswith("/") and len(parsed.path) > 1:
            parsed = parsed._replace(path=parsed.path.rstrip("/"))

        # Reconstruct the URL
        fixed_url = urllib.parse.urlunparse(parsed)

        # Final validation - make sure we have a valid netloc
        final_parsed = urllib.parse.urlparse(fixed_url)
        if not final_parsed.netloc or final_parsed.netloc in [".", "..", "..."]:
            return None

        # Check if netloc contains only dots or is otherwise invalid
        if re.match(r"^\.+$", final_parsed.netloc):
            return None

        return fixed_url

    @staticmethod
    def validate(value: str, _: str | None = None) -> str | None:
        """
        Check that a string is indeed verbatim to the input text.

        :param value: string value to assess.
        :param _: placeholder for text_input.
        :return: error message if the value is not in the input text, otherwise
            ``None``.
        """
        matched = match(value, rule="IRI")
        if matched is None:
            return ERR_LABEL_URL_IS_MALFORMED
        return None
