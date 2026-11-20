"""Renderer-independent descriptions of character animation capabilities."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class CharacterCapabilityProfile:
    """Capabilities available to the Animation Director for one character.

    Semantic IDs identify reusable clip capabilities. Procedural capabilities
    use the same semantic vocabulary but are resolved by the compiler.
    """

    character_id: str
    rig_type: str
    supported_channels: list[str] = field(default_factory=list)
    supported_semantic_ids: list[str] = field(default_factory=list)
    procedural_capabilities: list[str] = field(default_factory=list)
    facial_capabilities: list[str] = field(default_factory=list)
    gaze_capabilities: list[str] = field(default_factory=list)
    interaction_capabilities: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CharacterCapabilityProfile":
        if not isinstance(data, dict):
            raise TypeError("CharacterCapabilityProfile data must be a dictionary.")
        allowed = set(cls.__dataclass_fields__)
        unknown = set(data) - allowed
        if unknown:
            raise ValueError(f"Unknown CharacterCapabilityProfile fields: {', '.join(sorted(unknown))}")
        missing = {"character_id", "rig_type"} - set(data)
        if missing:
            raise ValueError(f"Missing CharacterCapabilityProfile fields: {', '.join(sorted(missing))}")
        for name in ("character_id", "rig_type"):
            if not isinstance(data[name], str):
                raise TypeError(f"'{name}' must be a string.")
        list_fields = allowed - {"character_id", "rig_type"}
        for name in list_fields:
            if name in data and (not isinstance(data[name], list) or not all(isinstance(x, str) for x in data[name])):
                raise TypeError(f"'{name}' must be a list of strings.")
        return cls(**data)

    @classmethod
    def from_json(cls, value: str) -> "CharacterCapabilityProfile":
        return cls.from_dict(json.loads(value))

    @classmethod
    def load_json(cls, path: str | Path) -> "CharacterCapabilityProfile":
        return cls.from_json(Path(path).read_text(encoding="utf-8"))
