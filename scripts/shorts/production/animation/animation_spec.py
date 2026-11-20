"""Renderer-independent animation output contracts."""

from __future__ import annotations

import json
from dataclasses import MISSING, asdict, dataclass, field
from pathlib import Path
from typing import Any


VALID_EXECUTION_MODES = {"clip", "procedural"}
VALID_ANIMATION_STATUSES = {"supported", "degraded", "unsupported"}
VALID_ENERGIES = {"low", "medium", "high"}
VALID_SPEEDS = {"slow", "normal", "fast"}
VALID_WEIGHTS = {"light", "normal", "heavy"}
VALID_INTENSITIES = {"subtle", "moderate", "exaggerated"}
VALID_TRANSITION_STYLES = {"smooth", "abrupt", "quick", "gradual"}


@dataclass
class AnimationMotionSpec:
    """Semantic movement request, independent of any rig or renderer."""

    semantic_id: str
    execution_mode: str
    description: str
    loop: bool = False
    parameters: dict[str, str | int | float | bool] = field(default_factory=dict)


@dataclass
class AnimationPerformanceSpec:
    """Stylistic qualities that shape how a motion is performed."""

    energy: str
    speed: str
    weight: str
    intensity: str
    emotion: str | None = None
    description: str | None = None


@dataclass
class AnimationTransitionSpec:
    """Desired transition into the current action."""

    source_action_id: str | None = None
    duration_frames: int = 6
    style: str = "smooth"
    description: str | None = None


@dataclass
class AnimationIssueSpec:
    """Structured diagnostic or documented fallback for an action."""

    code: str
    message: str
    required_capability: str | None = None
    fallback_description: str | None = None


@dataclass
class CharacterAnimationSpec:
    """Animation Director output for exactly one CharacterActionSpec."""

    id: str
    action_id: str
    character_id: str
    channel: str
    start_frame: int
    end_frame: int
    status: str
    motion: AnimationMotionSpec | None = None
    performance: AnimationPerformanceSpec | None = None
    transition_in: AnimationTransitionSpec | None = None
    issues: list[AnimationIssueSpec] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def save_json(self, path: str | Path) -> Path:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(self.to_json(), encoding="utf-8")
        return output

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CharacterAnimationSpec":
        if not isinstance(data, dict):
            raise TypeError("CharacterAnimationSpec data must be a dictionary.")
        allowed = {
            "id", "action_id", "character_id", "channel", "start_frame",
            "end_frame", "status", "motion", "performance", "transition_in", "issues",
        }
        unknown = set(data) - allowed
        if unknown:
            raise ValueError(f"Unknown CharacterAnimationSpec fields: {', '.join(sorted(unknown))}")
        required = {"id", "action_id", "character_id", "channel", "start_frame", "end_frame", "status"}
        missing = required - set(data)
        if missing:
            raise ValueError(f"Missing CharacterAnimationSpec fields: {', '.join(sorted(missing))}")

        payload = dict(data)
        payload["motion"] = _build_nested(AnimationMotionSpec, payload.get("motion"), "motion")
        payload["performance"] = _build_nested(AnimationPerformanceSpec, payload.get("performance"), "performance")
        payload["transition_in"] = _build_nested(AnimationTransitionSpec, payload.get("transition_in"), "transition_in")
        raw_issues = payload.get("issues", [])
        if not isinstance(raw_issues, list):
            raise TypeError("'issues' must be a list.")
        payload["issues"] = [_build_nested(AnimationIssueSpec, item, f"issues[{i}]") for i, item in enumerate(raw_issues)]
        for name in ("id", "action_id", "character_id", "channel", "status"):
            if not isinstance(payload[name], str):
                raise TypeError(f"'{name}' must be a string.")
        for name in ("start_frame", "end_frame"):
            if type(payload[name]) is not int:
                raise TypeError(f"'{name}' must be an integer.")
        return cls(**payload)

    @classmethod
    def from_json(cls, value: str) -> "CharacterAnimationSpec":
        return cls.from_dict(json.loads(value))

    @classmethod
    def load_json(cls, path: str | Path) -> "CharacterAnimationSpec":
        return cls.from_json(Path(path).read_text(encoding="utf-8"))


def _build_nested(record_type: type, value: Any, label: str) -> Any:
    if value is None:
        return None
    if isinstance(value, record_type):
        return value
    if not isinstance(value, dict):
        raise TypeError(f"'{label}' must be a dictionary or None.")
    allowed = set(record_type.__dataclass_fields__)
    unknown = set(value) - allowed
    if unknown:
        raise ValueError(f"Unknown fields in '{label}': {', '.join(sorted(unknown))}")
    required = {
        name for name, item in record_type.__dataclass_fields__.items()
        if item.default is item.default_factory and item.default_factory is __import__('dataclasses').MISSING
    }
    missing = required - set(value)
    if missing:
        raise ValueError(f"Missing fields in '{label}': {', '.join(sorted(missing))}")

    string_fields = {
        "semantic_id", "execution_mode", "energy", "speed",
        "weight", "intensity", "style", "code", "message",
    }
    optional_string_fields = {
        "emotion", "source_action_id", "fallback_description", "required_capability",
    }
    if record_type in (AnimationPerformanceSpec, AnimationTransitionSpec):
        optional_string_fields.add("description")
    for name, item in value.items():
        if name in string_fields and not isinstance(item, str):
            raise TypeError(f"'{label}.{name}' must be a string.")
        if name in optional_string_fields and item is not None and not isinstance(item, str):
            raise TypeError(f"'{label}.{name}' must be a string or None.")
        if name in {"loop"} and type(item) is not bool:
            raise TypeError(f"'{label}.{name}' must be a boolean.")
        if name == "duration_frames" and type(item) is not int:
            raise TypeError(f"'{label}.{name}' must be an integer.")
        if name == "parameters":
            if not isinstance(item, dict):
                raise TypeError(f"'{label}.parameters' must be a dictionary.")
            if any(not isinstance(key, str) or type(val) not in (str, int, float, bool) for key, val in item.items()):
                raise TypeError(f"'{label}.parameters' must contain scalar values with string keys.")
    return record_type(**value)
