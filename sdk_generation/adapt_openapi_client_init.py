"""Adds async imports to the openapi_client package."""  # noqa:INP001

import re
from pathlib import Path


def modify_init_file(file_path: Path) -> None:
    """
    Modify the __init__.py file to add async versions of imports.

    Args:
        file_path (str): Path to the __init__.py file

    """
    with file_path.open() as f:
        content = f.read()

    # First, we need to update the __all__ list to include async versions
    all_pattern = r"__all__\s*=\s*\[(.*?)\]"
    all_match = re.search(all_pattern, content, re.DOTALL)

    if all_match:
        all_content = all_match.group(1)
        # Extract existing items and add async versions
        items = re.findall(r'"([^"]*)"', all_content)
        async_items = []

        for item in items:
            if item.endswith("Api"):
                async_items.append(f'"{item}Async"')
            elif item == "ApiClient":
                async_items.append('"ApiClientAsync"')

        # Create new __all__ content
        all_items = [f'"{item}"' for item in items] + async_items
        new_all_content = "__all__ = [\n    " + ",\n    ".join(all_items) + ",\n]"

        content = re.sub(all_pattern, new_all_content, content, flags=re.DOTALL)

    # Now handle the TYPE_CHECKING block imports
    type_checking_pattern = r'(if __import__\("typing"\)\.TYPE_CHECKING:.*?)(else:)'
    type_checking_match = re.search(type_checking_pattern, content, re.DOTALL)

    if type_checking_match:
        type_checking_block = type_checking_match.group(1)

        # Find all API imports and create async versions
        api_imports = re.findall(
            r"from numind\.openapi_client\.api\.(\w+) import (\w+) as (\w+)",
            type_checking_block,
        )

        # Find ApiClient import
        client_import = re.search(
            (
                r"from numind\.openapi_client\.api_client import (ApiClient) as "
                r"(ApiClient)"
            ),
            type_checking_block,
        )

        async_imports = []

        # Add async API imports
        for module, class_name, alias in api_imports:
            async_import = (
                f"    from numind.openapi_client.api_async.{module} import "
                f"{class_name} as {alias}Async"
            )
            async_imports.append(async_import)

        # Add async ApiClient import
        if client_import:
            async_import = (
                "    from numind.openapi_client.api_client_async import ApiClient as "
                "ApiClientAsync"
            )
            async_imports.append(async_import)

        # Insert async imports after the existing imports
        if async_imports:
            async_imports_str = "\n" + "\n".join(async_imports)
            # Find the position just before 'else:'
            else_pos = content.find("else:", type_checking_match.start())
            content = content[:else_pos] + async_imports_str + "\n" + content[else_pos:]

    # Now handle the lazy loading block
    lazy_pattern = (
        r'(load\(\s*LazyModule\(\s*\*as_package\(__file__\),.*?""")(.*?)(""",)'
    )
    lazy_match = re.search(lazy_pattern, content, re.DOTALL)

    if lazy_match:
        lazy_imports = lazy_match.group(2)

        # Find all API imports and create async versions
        api_imports = re.findall(
            r"from numind\.openapi_client\.api\.(\w+) import (\w+) as (\w+)",
            lazy_imports,
        )

        # Find ApiClient import
        client_import = re.search(
            (
                r"from numind\.openapi_client\.api_client import (ApiClient) as "
                r"(ApiClient)"
            ),
            lazy_imports,
        )

        async_imports = []

        # Add async API imports
        for module, class_name, alias in api_imports:
            async_import = (
                f"from numind.openapi_client.api_async.{module} import {class_name} "
                f"as {alias}Async"
            )
            async_imports.append(async_import)

        # Add async ApiClient import
        if client_import:
            async_import = (
                "from numind.openapi_client.api_client_async import ApiClient as "
                "ApiClientAsync"
            )
            async_imports.append(async_import)

        # Insert async imports
        if async_imports:
            async_imports_str = "\n" + "\n".join(async_imports)
            new_lazy_imports = lazy_imports + async_imports_str
            content = content.replace(lazy_imports, new_lazy_imports)

    with file_path.open("w") as f:
        f.write(content)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Dataset creation script")
    parser.add_argument(
        "--init-path", type=str, default="src/numind/openapi_client/__init__.py"
    )
    args = vars(parser.parse_args())

    modify_init_file(
        Path(args["init_path"]),
    )
