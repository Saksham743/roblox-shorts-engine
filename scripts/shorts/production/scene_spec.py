
"""Renderer-independent production specification for Roblox Shorts."""

from __future__ import annotations

import json
import types

from dataclasses import (
    MISSING,
    asdict,
    dataclass,
    field,
    fields,
)
from pathlib import Path
from typing import (
    Any,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)


SCENE_SPEC_VERSION = "1.0.0"


# ---------------------------------------------------------------------
# Supported vocabularies
# ---------------------------------------------------------------------

VALID_CAMERA_FRAMINGS = {
    "extreme_wide",
    "wide",
    "medium",
    "close_up",
    "extreme_close_up",
}

VALID_CAMERA_ANGLES = {
    "eye_level",
    "high_angle",
    "low_angle",
    "bird_eye",
    "dutch",
}

VALID_CAMERA_MOVEMENTS = {
    "static",
    "pan",
    "tilt",
    "dolly",
    "tracking",
    "crane",
    "orbit",
    "zoom",
    "handheld",
    "slow_push_in",
    "slow_pull_back",
}

VALID_TIMES_OF_DAY = {
    "dawn",
    "morning",
    "day",
    "afternoon",
    "evening",
    "dusk",
    "night",
}


# ---------------------------------------------------------------------
# Specification data models
# ---------------------------------------------------------------------

@dataclass
class ProjectSpec:
    title: str
    source_story: str
    fps: int = 30
    width: int = 1080
    height: int = 1920
    duration_frames: int = 300
    visual_style: str = "Roblox-style 3D animation"


@dataclass
class CharacterSpec:
    id: str
    name: str
    role: str
    appearance: str
    outfit: str
    design_reference: str | None = None


@dataclass
class EnvironmentSpec:
    id: str
    name: str
    description: str
    environment_type: str = "custom"
    required_assets: list[str] = field(default_factory=list)


@dataclass
class SceneSpec:
    id: str
    name: str
    description: str
    start_frame: int
    end_frame: int
    environment_id: str
    time_of_day: str | None = None
    lighting_description: str | None = None


@dataclass
class EventSpec:
    id: str
    scene_id: str
    name: str
    description: str
    start_frame: int
    end_frame: int
    action: str
    actor_ids: list[str] = field(default_factory=list)
    target: str | None = None


@dataclass
class ShotSpec:
    id: str
    scene_id: str
    start_frame: int
    end_frame: int
    subject_ids: list[str] = field(default_factory=list)
    framing: str = "medium"
    angle: str = "eye_level"
    movement: str = "static"
    camera_intent: str = ""
    target_description: str | None = None


@dataclass
class SoundEffectSpec:
    id: str
    name: str
    start_frame: int
    end_frame: int
    asset_path: str | None = None


@dataclass
class AudioSpec:
    narration_text: str | None = None
    narration_audio_path: str | None = None
    music_description: str | None = None
    music_asset_path: str | None = None
    sound_effects: list[SoundEffectSpec] = field(default_factory=list)


# ---------------------------------------------------------------------
# Main specification
# ---------------------------------------------------------------------

@dataclass
class SceneSpecification:
    project: ProjectSpec
    characters: list[CharacterSpec]
    environments: list[EnvironmentSpec]
    scenes: list[SceneSpec]
    events: list[EventSpec]
    shots: list[ShotSpec]
    audio: AudioSpec = field(default_factory=AudioSpec)
    schema_version: str = SCENE_SPEC_VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=False,
        )

    def save_json(self, path: str | Path) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_path.write_text(
            self.to_json(),
            encoding="utf-8",
        )

        return output_path

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SceneSpecification:
        """Reconstruct a specification while validating structure and types."""

        if not isinstance(data, dict):
            raise TypeError(
                "Scene specification data must be a dictionary."
            )

        allowed_fields = {
            "project",
            "characters",
            "environments",
            "scenes",
            "events",
            "shots",
            "audio",
            "schema_version",
        }

        required_fields = {
            "project",
            "characters",
            "environments",
            "scenes",
            "events",
            "shots",
        }

        unknown_fields = set(data) - allowed_fields

        if unknown_fields:
            raise ValueError(
                "Unknown SceneSpecification fields: "
                + ", ".join(
                    sorted(str(item) for item in unknown_fields)
                )
            )

        missing_fields = required_fields - set(data)

        if missing_fields:
            raise ValueError(
                "Missing required SceneSpecification fields: "
                + ", ".join(sorted(missing_fields))
            )

        schema_version = data.get(
            "schema_version",
            SCENE_SPEC_VERSION,
        )

        if not isinstance(schema_version, str):
            raise TypeError("'schema_version' must be a string.")

        if schema_version != SCENE_SPEC_VERSION:
            raise ValueError(
                f"Unsupported SceneSpec version '{schema_version}'. "
                f"Expected '{SCENE_SPEC_VERSION}'."
            )

        def validate_value(
            value: Any,
            expected_type: Any,
            path: str,
        ) -> None:
            """Validate a value against its declared type annotation."""

            origin = get_origin(expected_type)
            args = get_args(expected_type)

            # Optional and Union types.
            if origin in (Union, types.UnionType):

                if (
                    any(arg is type(None) for arg in args)
                    and value is None
                ):
                    return

                for possible_type in args:
                    if possible_type is type(None):
                        continue

                    try:
                        validate_value(
                            value,
                            possible_type,
                            path,
                        )
                        return
                    except TypeError:
                        continue

                raise TypeError(
                    f"'{path}' has an invalid type. "
                    f"Expected {expected_type}, "
                    f"got {type(value).__name__}."
                )

            # Lists and their individual elements.
            if origin is list:

                if not isinstance(value, list):
                    raise TypeError(
                        f"'{path}' must be a list, "
                        f"got {type(value).__name__}."
                    )

                item_type = args[0] if args else Any

                for index, item in enumerate(value):
                    validate_value(
                        item,
                        item_type,
                        f"{path}[{index}]",
                    )

                return

            if expected_type is Any:
                return

            # bool is a subclass of int in Python.
            # Use exact type checking for integer fields.
            if expected_type is int:

                if type(value) is not int:
                    raise TypeError(
                        f"'{path}' must be an integer, "
                        f"got {type(value).__name__}."
                    )

                return

            if expected_type is bool:

                if type(value) is not bool:
                    raise TypeError(
                        f"'{path}' must be a boolean, "
                        f"got {type(value).__name__}."
                    )

                return

            if not isinstance(value, expected_type):
                raise TypeError(
                    f"'{path}' must be "
                    f"{expected_type.__name__}, "
                    f"got {type(value).__name__}."
                )

        def build_record(
            record_type: type,
            payload: Any,
            path: str,
        ) -> Any:
            """Validate and construct one dataclass record."""

            if not isinstance(payload, dict):
                raise TypeError(
                    f"'{path}' must be a dictionary."
                )

            record_fields = {
                item.name: item
                for item in fields(record_type)
            }

            unknown = set(payload) - set(record_fields)

            if unknown:
                raise ValueError(
                    f"Unknown fields in '{path}': "
                    + ", ".join(
                        sorted(str(item) for item in unknown)
                    )
                )

            missing = {
                name
                for name, item in record_fields.items()
                if (
                    item.default is MISSING
                    and item.default_factory is MISSING
                    and name not in payload
                )
            }

            if missing:
                raise ValueError(
                    f"Missing required fields in '{path}': "
                    + ", ".join(sorted(missing))
                )

            type_hints = get_type_hints(record_type)

            for name, value in payload.items():
                validate_value(
                    value,
                    type_hints[name],
                    f"{path}.{name}",
                )

            return record_type(**payload)

        def build_record_list(
            record_type: type,
            payload: Any,
            path: str,
        ) -> list[Any]:
            """Validate and construct a list of dataclass records."""

            if not isinstance(payload, list):
                raise TypeError(
                    f"'{path}' must be a list."
                )

            return [
                build_record(
                    record_type,
                    item,
                    f"{path}[{index}]",
                )
                for index, item in enumerate(payload)
            ]

        project = build_record(
            ProjectSpec,
            data["project"],
            "project",
        )

        characters = build_record_list(
            CharacterSpec,
            data["characters"],
            "characters",
        )

        environments = build_record_list(
            EnvironmentSpec,
            data["environments"],
            "environments",
        )

        scenes = build_record_list(
            SceneSpec,
            data["scenes"],
            "scenes",
        )

        events = build_record_list(
            EventSpec,
            data["events"],
            "events",
        )

        shots = build_record_list(
            ShotSpec,
            data["shots"],
            "shots",
        )

        audio_data = data.get("audio", {})

        if not isinstance(audio_data, dict):
            raise TypeError("'audio' must be a dictionary.")

        audio_data = dict(audio_data)

        sound_effect_data = audio_data.pop(
            "sound_effects",
            [],
        )

        sound_effects = build_record_list(
            SoundEffectSpec,
            sound_effect_data,
            "audio.sound_effects",
        )

        audio_data["sound_effects"] = sound_effects

        audio = build_record(
            AudioSpec,
            audio_data,
            "audio",
        )

        return cls(
            project=project,
            characters=characters,
            environments=environments,
            scenes=scenes,
            events=events,
            shots=shots,
            audio=audio,
            schema_version=schema_version,
        )

    @classmethod
    def load_json(
        cls,
        path: str | Path,
    ) -> SceneSpecification:
        """Load a specification from a JSON file."""

        input_path = Path(path)

        if not input_path.is_file():
            raise FileNotFoundError(
                f"Scene specification file not found: {input_path}"
            )

        data = json.loads(
            input_path.read_text(encoding="utf-8")
        )

        return cls.from_dict(data)


# ---------------------------------------------------------------------
# Semantic and timeline validation
# ---------------------------------------------------------------------

def validate_scene_spec(
    spec: SceneSpecification,
) -> list[str]:
    """Validate timeline consistency and specification references."""

    errors: list[str] = []

    def check_frame_range(
        start_frame: int,
        end_frame: int,
        label: str,
    ) -> None:

        if start_frame < 0:
            errors.append(
                f"{label} starts before frame 0."
            )

        if end_frame <= start_frame:
            errors.append(
                f"{label} must have end_frame greater than start_frame."
            )

        if end_frame > spec.project.duration_frames:
            errors.append(
                f"{label} exceeds project duration."
            )

    def check_unique_ids(
        items: list[Any],
        label: str,
    ) -> None:

        seen: set[str] = set()

        for item in items:

            if item.id in seen:
                errors.append(
                    f"Found duplicate ID '{item.id}' in {label}."
                )

            seen.add(item.id)

    def check_non_empty_id(
        item: Any,
        label: str,
    ) -> None:

        if not isinstance(item.id, str) or not item.id.strip():
            errors.append(
                f"{label} must have a non-empty string ID."
            )

    def check_non_empty_text(
        value: str,
        label: str,
    ) -> None:

        if not isinstance(value, str) or not value.strip():
            errors.append(
                f"{label} must be a non-empty string."
            )

    def check_allowed_value(
        value: str,
        allowed_values: set[str],
        label: str,
    ) -> None:

        if value not in allowed_values:
            errors.append(
                f"{label} has unsupported value '{value}'. "
                f"Allowed values: "
                f"{', '.join(sorted(allowed_values))}."
            )

    def check_optional_time_of_day(
        value: str | None,
        label: str,
    ) -> None:

        if value is not None:
            check_allowed_value(
                value,
                VALID_TIMES_OF_DAY,
                label,
            )

    def check_contiguous_timeline(
        items: list[Any],
        label: str,
    ) -> None:

        ordered = sorted(
            items,
            key=lambda item: item.start_frame,
        )

        if not ordered:
            return

        if ordered[0].start_frame != 0:
            errors.append(
                f"{label} timeline must start at frame 0."
            )

        for previous, current in zip(
            ordered,
            ordered[1:],
        ):

            if current.start_frame > previous.end_frame:
                errors.append(
                    f"{label} timeline gap between "
                    f"'{previous.id}' and '{current.id}'."
                )

            elif current.start_frame < previous.end_frame:
                errors.append(
                    f"{label} timeline overlap between "
                    f"'{previous.id}' and '{current.id}'."
                )

        if ordered[-1].end_frame != spec.project.duration_frames:
            errors.append(
                f"{label} timeline must end at project duration."
            )

    # -------------------------------------------------------------
    # Project validation
    # -------------------------------------------------------------

    check_non_empty_text(
        spec.project.title,
        "Project title",
    )

    check_non_empty_text(
        spec.project.source_story,
        "Source story",
    )

    check_non_empty_text(
        spec.project.visual_style,
        "Project visual_style",
    )

    if spec.project.fps <= 0:
        errors.append(
            "Project FPS must be greater than zero."
        )

    if spec.project.width <= 0 or spec.project.height <= 0:
        errors.append(
            "Project resolution must be positive."
        )

    if spec.project.duration_frames <= 0:
        errors.append(
            "Project duration_frames must be greater than zero."
        )

    if not spec.scenes:
        errors.append(
            "Specification must contain at least one scene."
        )

    if not spec.shots:
        errors.append(
            "Specification must contain at least one camera shot."
        )

    # -------------------------------------------------------------
    # Required text validation
    # -------------------------------------------------------------

    for character in spec.characters:

        check_non_empty_text(
            character.name,
            f"Character '{character.id}' name",
        )

        check_non_empty_text(
            character.role,
            f"Character '{character.id}' role",
        )

        check_non_empty_text(
            character.appearance,
            f"Character '{character.id}' appearance",
        )

        check_non_empty_text(
            character.outfit,
            f"Character '{character.id}' outfit",
        )

    for environment in spec.environments:

        check_non_empty_text(
            environment.name,
            f"Environment '{environment.id}' name",
        )

        check_non_empty_text(
            environment.description,
            f"Environment '{environment.id}' description",
        )

        check_non_empty_text(
            environment.environment_type,
            f"Environment '{environment.id}' type",
        )

    for scene in spec.scenes:

        check_non_empty_text(
            scene.name,
            f"Scene '{scene.id}' name",
        )

        check_non_empty_text(
            scene.description,
            f"Scene '{scene.id}' description",
        )

        check_optional_time_of_day(
            scene.time_of_day,
            f"Scene '{scene.id}' time_of_day",
        )

    for event in spec.events:

        check_non_empty_text(
            event.name,
            f"Event '{event.id}' name",
        )

        check_non_empty_text(
            event.description,
            f"Event '{event.id}' description",
        )

        check_non_empty_text(
            event.action,
            f"Event '{event.id}' action",
        )

    for sound in spec.audio.sound_effects:

        check_non_empty_text(
            sound.name,
            f"Sound effect '{sound.id}' name",
        )

    # -------------------------------------------------------------
    # Unique ID validation
    # -------------------------------------------------------------

    check_unique_ids(spec.characters, "characters")
    check_unique_ids(spec.environments, "environments")
    check_unique_ids(spec.scenes, "scenes")
    check_unique_ids(spec.events, "events")
    check_unique_ids(spec.shots, "shots")
    check_unique_ids(
        spec.audio.sound_effects,
        "sound effects",
    )

    # -------------------------------------------------------------
    # Non-empty ID validation
    # -------------------------------------------------------------

    for item in spec.characters:
        check_non_empty_id(item, "Character")

    for item in spec.environments:
        check_non_empty_id(item, "Environment")

    for item in spec.scenes:
        check_non_empty_id(item, "Scene")

    for item in spec.events:
        check_non_empty_id(item, "Event")

    for item in spec.shots:
        check_non_empty_id(item, "Shot")

    for item in spec.audio.sound_effects:
        check_non_empty_id(item, "Sound effect")

    # -------------------------------------------------------------
    # Camera vocabulary validation
    # -------------------------------------------------------------

    for shot in spec.shots:

        check_allowed_value(
            shot.framing,
            VALID_CAMERA_FRAMINGS,
            f"Shot '{shot.id}' framing",
        )

        check_allowed_value(
            shot.angle,
            VALID_CAMERA_ANGLES,
            f"Shot '{shot.id}' angle",
        )

        check_allowed_value(
            shot.movement,
            VALID_CAMERA_MOVEMENTS,
            f"Shot '{shot.id}' movement",
        )

    # -------------------------------------------------------------
    # Reference collections
    # -------------------------------------------------------------

    character_ids = {
        character.id
        for character in spec.characters
    }

    environment_ids = {
        environment.id
        for environment in spec.environments
    }

    scene_by_id = {
        scene.id: scene
        for scene in spec.scenes
    }

    # -------------------------------------------------------------
    # Scene validation
    # -------------------------------------------------------------

    for scene in spec.scenes:

        check_frame_range(
            scene.start_frame,
            scene.end_frame,
            f"Scene '{scene.id}'",
        )

        if scene.environment_id not in environment_ids:
            errors.append(
                f"Scene '{scene.id}' references unknown environment "
                f"'{scene.environment_id}'."
            )

    check_contiguous_timeline(
        spec.scenes,
        "Scene",
    )

    # -------------------------------------------------------------
    # Event validation
    # -------------------------------------------------------------

    for event in spec.events:

        check_frame_range(
            event.start_frame,
            event.end_frame,
            f"Event '{event.id}'",
        )

        parent_scene = scene_by_id.get(event.scene_id)

        if parent_scene is None:
            errors.append(
                f"Event '{event.id}' references unknown scene "
                f"'{event.scene_id}'."
            )

        elif (
            event.start_frame < parent_scene.start_frame
            or event.end_frame > parent_scene.end_frame
        ):
            errors.append(
                f"Event '{event.id}' falls outside scene "
                f"'{parent_scene.id}'."
            )

        for actor_id in event.actor_ids:

            if actor_id not in character_ids:
                errors.append(
                    f"Event '{event.id}' references unknown character "
                    f"'{actor_id}'."
                )

    # -------------------------------------------------------------
    # Shot validation
    # -------------------------------------------------------------

    for shot in spec.shots:

        check_frame_range(
            shot.start_frame,
            shot.end_frame,
            f"Shot '{shot.id}'",
        )

        parent_scene = scene_by_id.get(shot.scene_id)

        if parent_scene is None:
            errors.append(
                f"Shot '{shot.id}' references unknown scene "
                f"'{shot.scene_id}'."
            )

        elif (
            shot.start_frame < parent_scene.start_frame
            or shot.end_frame > parent_scene.end_frame
        ):
            errors.append(
                f"Shot '{shot.id}' falls outside scene "
                f"'{parent_scene.id}'."
            )

        for subject_id in shot.subject_ids:

            if subject_id not in character_ids:
                errors.append(
                    f"Shot '{shot.id}' references unknown character "
                    f"'{subject_id}'."
                )

    check_contiguous_timeline(
        spec.shots,
        "Shot",
    )

    # -------------------------------------------------------------
    # Sound effect validation
    # -------------------------------------------------------------

    for sound in spec.audio.sound_effects:

        check_frame_range(
            sound.start_frame,
            sound.end_frame,
            f"Sound effect '{sound.id}'",
        )

    return errors
