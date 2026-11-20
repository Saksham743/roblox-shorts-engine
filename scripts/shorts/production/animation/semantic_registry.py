
"""Canonical, renderer-independent semantic animation registry."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .animation_spec import VALID_EXECUTION_MODES


VALID_ANIMATION_CHANNELS = frozenset({
    "locomotion",
    "body",
    "gesture",
    "facial",
    "gaze",
    "interaction",
    "prop",
})

_SEMANTIC_ID_PATTERN = re.compile(
    r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+$"
)


@dataclass(frozen=True)
class SemanticAnimationDefinition:
    """Immutable definition of a canonical animation meaning."""

    semantic_id: str
    category: str
    channel: str
    description: str
    execution_modes: tuple[str, ...]
    loopable: bool
    required_capabilities: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        self._validate_text("semantic_id", self.semantic_id)
        self._validate_text("category", self.category)
        self._validate_text("description", self.description)

        if not _SEMANTIC_ID_PATTERN.fullmatch(self.semantic_id):
            raise ValueError(
                f"Invalid semantic ID '{self.semantic_id}'. "
                "Use lowercase dot-separated identifiers."
            )

        if self.channel not in VALID_ANIMATION_CHANNELS:
            raise ValueError(
                f"Invalid animation channel '{self.channel}'. "
                f"Expected one of: {', '.join(sorted(VALID_ANIMATION_CHANNELS))}."
            )

        if not isinstance(self.execution_modes, tuple):
            raise TypeError("'execution_modes' must be a tuple.")

        if not self.execution_modes:
            raise ValueError("'execution_modes' cannot be empty.")

        invalid_modes = set(self.execution_modes) - VALID_EXECUTION_MODES
        if invalid_modes:
            raise ValueError(
                f"Invalid execution modes: {', '.join(sorted(invalid_modes))}."
            )

        if len(set(self.execution_modes)) != len(self.execution_modes):
            raise ValueError("'execution_modes' cannot contain duplicates.")

        if type(self.loopable) is not bool:
            raise TypeError("'loopable' must be a boolean.")

        self._validate_string_tuple(
            "required_capabilities",
            self.required_capabilities,
        )
        self._validate_string_tuple("tags", self.tags)

    @staticmethod
    def _validate_text(field_name: str, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"'{field_name}' must be a string.")

        if not value.strip():
            raise ValueError(f"'{field_name}' cannot be empty.")

    @staticmethod
    def _validate_string_tuple(
        field_name: str,
        values: tuple[str, ...],
    ) -> None:
        if not isinstance(values, tuple):
            raise TypeError(f"'{field_name}' must be a tuple.")

        for value in values:
            if not isinstance(value, str):
                raise TypeError(
                    f"Every item in '{field_name}' must be a string."
                )

            if not value.strip():
                raise ValueError(
                    f"'{field_name}' cannot contain empty strings."
                )


class SemanticAnimationRegistry:
    """Stores and retrieves canonical semantic animation definitions."""

    def __init__(self) -> None:
        self._definitions: dict[str, SemanticAnimationDefinition] = {}

    def register(self, definition: SemanticAnimationDefinition) -> None:
        """Register a new semantic animation definition."""

        if not isinstance(definition, SemanticAnimationDefinition):
            raise TypeError(
                "'definition' must be a SemanticAnimationDefinition."
            )

        semantic_id = definition.semantic_id

        if semantic_id in self._definitions:
            raise ValueError(
                f"Semantic animation '{semantic_id}' is already registered."
            )

        self._definitions[semantic_id] = definition

    def get(self, semantic_id: str) -> SemanticAnimationDefinition:
        """Retrieve a definition by its semantic ID."""

        if not isinstance(semantic_id, str):
            raise TypeError("'semantic_id' must be a string.")

        try:
            return self._definitions[semantic_id]
        except KeyError:
            raise KeyError(
                f"Unknown semantic animation: '{semantic_id}'."
            ) from None

    def get_by_channel(
        self,
        channel: str,
    ) -> tuple[SemanticAnimationDefinition, ...]:
        """Return all definitions belonging to a channel."""

        if channel not in VALID_ANIMATION_CHANNELS:
            raise ValueError(f"Unknown animation channel: '{channel}'.")

        return tuple(
            definition
            for definition in self._definitions.values()
            if definition.channel == channel
        )

    def search_by_tags(
        self,
        tags: set[str] | frozenset[str],
    ) -> tuple[SemanticAnimationDefinition, ...]:
        """Return definitions matching at least one supplied tag."""

        if not isinstance(tags, (set, frozenset)):
            raise TypeError("'tags' must be a set or frozenset.")

        if not all(isinstance(tag, str) for tag in tags):
            raise TypeError("Every search tag must be a string.")

        requested_tags = {tag.casefold() for tag in tags}

        return tuple(
            definition
            for definition in self._definitions.values()
            if requested_tags.intersection(
                tag.casefold() for tag in definition.tags
            )
        )

    def all(self) -> tuple[SemanticAnimationDefinition, ...]:
        """Return all registered definitions in registration order."""

        return tuple(self._definitions.values())

    def __len__(self) -> int:
        return len(self._definitions)

    def __contains__(self, semantic_id: object) -> bool:
        return semantic_id in self._definitions
