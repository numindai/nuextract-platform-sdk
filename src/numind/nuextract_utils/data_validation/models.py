"""Classes for data validation."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import orjson


@dataclass
class ErrorJson:
    """Error in a JSON."""

    path: list[str | int]
    error_message: str
    value_erroneous: str | int | float | list | None = None
    value_fixed: str | int | float | list | None = None
    node_deleted: bool | None = None
    # TODO handle cases like array squeezed...

    def to_dict(self) -> dict:
        """
        Return the instance as a dictionary.

        :return: dictionary of the instance.
        """
        return asdict(self)

    def to_json(self) -> str:
        """
        Return the instance as a JSON string.

        :return: JSON string of the instance.
        """
        return orjson.dumps(self.to_dict()).decode()

    @classmethod
    def from_json(cls, s: str) -> ErrorJson:
        """
        Return the instance of a JSON string.

        :param s: JSON string to create an instance from.
        :return: instance of the provided JSON string.
        """
        return cls(**orjson.loads(s))
