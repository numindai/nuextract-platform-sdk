"""Utilities for types."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator, Sequence


class ClassCachedProperty:
    """
    A descriptor for class-level cached properties.

    It invalidates when the source value changes.
    """

    def __init__(
        self,
        source_attr: str,
        transform_func: Callable[[Any], Any] | None = None,
        cache_attr_name: str | None = None,
    ) -> None:
        self.source_attr = source_attr
        self.transform_func = transform_func or (lambda x: x)
        if cache_attr_name is None:
            self.cache_attr = f"_{source_attr}_cached"
        else:
            self.cache_attr = cache_attr_name
        self.hash_attr = f"_{source_attr}_hash"

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, obj: object, objtype: type[Any] | None = None) -> Any:  # noqa:ANN401
        if objtype is None:
            return self

        # Get the source data
        source_data = getattr(objtype, self.source_attr)

        # Calculate current hash of source data
        try:
            current_hash = hash(frozenset(source_data))
        except TypeError:
            # Fallback for unhashable types
            current_hash = hash(str(sorted(source_data)))

        # Check if we have cached data and if source hasn't changed
        if (
            hasattr(objtype, self.cache_attr)
            and hasattr(objtype, self.hash_attr)
            and getattr(objtype, self.hash_attr) == current_hash
        ):
            return getattr(objtype, self.cache_attr)

        # Source has changed or no cache exists, recalculate
        transformed_data = self.transform_func(source_data)

        # Cache the result and hash
        setattr(objtype, self.cache_attr, transformed_data)
        setattr(objtype, self.hash_attr, current_hash)

        return transformed_data


class MappingInterface:
    """
    A user-friendly, read-only associative mapping.

    This class can be instantiated directly from data using the `from_data`
    classmethod, or used by other classes that construct the data structures themselves.
    """

    def __init__(
        self,
        group_names: dict[str, int],
        groups_list: list[tuple[Any, ...]],
        index_map: dict[Any, int],
    ) -> None:
        """Initialize the mapping with pre-built data structures."""
        self.group_names = group_names
        self._groups = groups_list
        self._index = index_map
        # Pre-calculate and cache the hash for efficiency
        self._hash = hash(tuple(self._groups))

    @classmethod
    def from_data(cls, **named_data_lists: Sequence[Any]) -> MappingInterface:
        """
        Create a mapping directly from named data lists (factory).

        This is the common logic for building the mapping structures.
        """
        if not named_data_lists:
            msg = "At least one named data list must be provided."
            raise ValueError(msg)

        group_names_list = list(named_data_lists.keys())
        source_data_lists = list(named_data_lists.values())

        # 1. Create the primary data storage (list of associated groups)
        groups_list = list(zip(*source_data_lists))
        group_names_map = {name: idx for idx, name in enumerate(group_names_list)}

        # 2. Create the index dictionary (maps each item -> group_index)
        index_map = {}
        for i, group in enumerate(groups_list):
            for item in group:
                index_map[item] = i
                # Also index lowercase versions for case-insensitive lookups
                if isinstance(item, str):
                    index_map[item.lower()] = i

        return cls(group_names_map, groups_list, index_map)

    def get_group(self, key: Any) -> tuple[Any, ...] | None:  # noqa:ANN401
        """
        Retrieve the entire group of associated values for a given key.

        Returns None if the key is not found.

        This performs the efficient, two-step lookup:
        1. Find the group's index in the hash map (O(1)).
        2. Retrieve the group from the list by its index (O(1)).
        """
        group_index = self._index.get(key)
        if group_index is not None:
            return self._groups[group_index]
        return None

    def __getitem__(self, key: Any) -> tuple[Any, ...]:  # noqa:ANN401
        """Allow dictionary-style access, e.g., mapping['USA']."""
        group = self.get_group(key)
        if group is None:
            msg = f"Key '{key}' not found in any of the associated mappings."
            raise KeyError(msg)
        return group

    def __iter__(self) -> Iterator[tuple[Any, ...]]:
        """Return an iterator over the groups in the mapping."""
        return iter(self._groups)

    def __eq__(self, other: object) -> bool:
        """Two mappings are equal if they contain the same groups."""
        if not isinstance(other, MappingInterface):
            return NotImplemented
        return self._groups == other._groups

    def __hash__(self) -> int:
        """Provide a hash based on the immutable content of the groups."""
        return self._hash

    def __repr__(self) -> str:
        return f"<MappingInterface with {len(self._groups)} groups>"


class AssociativeMapping:
    """
    Descriptor creating a cached, index-based associative mapping.

    The mapping is built from multiple source attributes on a class and is automatically
    rebuilt if any of the source attributes change.
    """

    def __init__(self, *source_attrs: str) -> None:
        """
        Initialize the descriptor with the names of the source attributes.

        Used to monitor on the host class.
        """
        if not source_attrs:
            msg = "At least one source attribute must be provided."
            raise ValueError(msg)
        self.source_attrs = source_attrs
        self.name = ""
        self.cache_attr = ""
        self.hash_attr = ""

    def __set_name__(self, owner: type, name: str) -> None:
        """
        Set the names for the internal cache attributes to avoid collisions.

        Called when the descriptor is assigned to a class.
        """
        self.name = name
        self.cache_attr = f"_{name}_cached_mapping"
        self.hash_attr = f"_{name}_source_hash"

    def _build_mapping(self, owner: type) -> MappingInterface:
        """
        Construct the actual mapping data structures.

        This method is called only when the cache is invalid.
        """
        # Create a dictionary of {name: data_list} to pass to the factory
        named_data_lists = {attr: getattr(owner, attr) for attr in self.source_attrs}
        # Use the common factory to build the interface object
        return MappingInterface.from_data(**named_data_lists)

    def __get__(self, obj: object, owner: type[Any]) -> MappingInterface:
        """
        Handle access to the descriptor attribute (e.g., Country.country_data).

        Implements the caching and synchronization logic.
        """
        # This descriptor works on the class, not on instances.
        if owner is None:
            return self

        # Calculate a stable hash of the current source data.
        # We convert each source to a tuple to make it hashable.
        try:
            source_tuples = tuple(
                tuple(getattr(owner, attr)) for attr in self.source_attrs
            )
            current_hash = hash(source_tuples)
        except TypeError:
            # Fallback for unhashable data like sets
            source_tuples = tuple(
                tuple(sorted(getattr(owner, attr))) for attr in self.source_attrs
            )
            current_hash = hash(source_tuples)

        # Check if a cache exists and if the source data hasn't changed.
        if (
            hasattr(owner, self.cache_attr)
            and getattr(owner, self.hash_attr, None) == current_hash
        ):
            # Cache is valid, return the cached mapping object.
            return getattr(owner, self.cache_attr)

        # Cache is invalid (or doesn't exist), so we rebuild.
        new_mapping = self._build_mapping(owner)

        # Store the newly created mapping and the new hash on the class.
        setattr(owner, self.cache_attr, new_mapping)
        setattr(owner, self.hash_attr, current_hash)

        return new_mapping
