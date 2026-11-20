
"""Structural and cross-reference validation for animation plans."""

from __future__ import annotations

from collections import Counter
from typing import Iterable

from ..scene_spec import CharacterActionSpec
from .animation_spec import (
    VALID_ANIMATION_STATUSES,
    VALID_ENERGIES,
    VALID_EXECUTION_MODES,
    VALID_INTENSITIES,
    VALID_SPEEDS,
    VALID_TRANSITION_STYLES,
    VALID_WEIGHTS,
    AnimationMotionSpec,
    CharacterAnimationSpec,
)
from .capability_profile import CharacterCapabilityProfile
from .semantic_catalog import build_default_catalog


def validate_animation_spec(spec: CharacterAnimationSpec) -> list[str]:
    """Validate one animation output without needing a SceneSpec or renderer."""
    errors: list[str] = []

    for name in ("id", "action_id", "character_id", "channel"):
        value = getattr(spec, name)
        if not isinstance(value, str) or not value.strip():
            errors.append(
                f"CharacterAnimationSpec {name} must be a non-empty string."
            )

    if type(spec.start_frame) is not int or type(spec.end_frame) is not int:
        errors.append("Animation frame boundaries must be integers.")
    elif spec.start_frame < 0 or spec.end_frame <= spec.start_frame:
        errors.append(
            "Animation frame range must start at or after zero and have positive duration."
        )

    if spec.status not in VALID_ANIMATION_STATUSES:
        errors.append(f"Unsupported animation status '{spec.status}'.")

    if spec.status == "unsupported":
        if spec.motion is not None or spec.performance is not None:
            errors.append(
                "Unsupported animation must not contain motion or performance instructions."
            )
        if not spec.issues:
            errors.append("Unsupported animation must include at least one issue.")
    else:
        if spec.motion is None:
            errors.append("Supported or degraded animation must include motion.")
        if spec.performance is None:
            errors.append("Supported or degraded animation must include performance.")

        if spec.motion is not None:
            errors.extend(_validate_motion(spec.motion))

        if spec.performance is not None:
            performance = spec.performance
            for field, allowed in (
                ("energy", VALID_ENERGIES),
                ("speed", VALID_SPEEDS),
                ("weight", VALID_WEIGHTS),
                ("intensity", VALID_INTENSITIES),
            ):
                if getattr(performance, field) not in allowed:
                    errors.append(
                        f"Unsupported performance {field} "
                        f"'{getattr(performance, field)}'."
                    )

    if spec.status == "degraded" and not any(
        issue.fallback_description and issue.fallback_description.strip()
        for issue in spec.issues
    ):
        errors.append(
            "Degraded animation must document its fallback in an issue."
        )

    if spec.transition_in is not None:
        transition = spec.transition_in
        if (
            type(transition.duration_frames) is not int
            or transition.duration_frames < 0
        ):
            errors.append(
                "Transition duration_frames must be a non-negative integer."
            )
        if transition.style not in VALID_TRANSITION_STYLES:
            errors.append(
                f"Unsupported transition style '{transition.style}'."
            )

    for issue in spec.issues:
        if not issue.code.strip():
            errors.append("Animation issue code must not be empty.")
        if not issue.message.strip():
            errors.append("Animation issue message must not be empty.")

    return errors


def _validate_motion(motion: AnimationMotionSpec) -> list[str]:
    errors: list[str] = []

    if not motion.semantic_id.strip():
        errors.append("Animation semantic_id must not be empty.")

    if motion.execution_mode not in VALID_EXECUTION_MODES:
        errors.append(
            f"Unsupported animation execution_mode '{motion.execution_mode}'."
        )

    if not motion.description.strip():
        errors.append("Animation motion description must not be empty.")

    if not isinstance(motion.parameters, dict):
        errors.append("Animation motion parameters must be a dictionary.")
    else:
        for key, value in motion.parameters.items():
            if not isinstance(key, str) or not key.strip():
                errors.append(
                    "Animation parameter names must be non-empty strings."
                )
            if type(value) not in (str, int, float, bool):
                errors.append(
                    f"Animation parameter '{key}' must have a scalar value."
                )

    return errors


def validate_capability_profile(
    profile: CharacterCapabilityProfile,
) -> list[str]:
    errors: list[str] = []

    if not profile.character_id.strip():
        errors.append("Capability profile character_id must not be empty.")

    if not profile.rig_type.strip():
        errors.append("Capability profile rig_type must not be empty.")

    for field in (
        "supported_channels",
        "supported_semantic_ids",
        "supported_capabilities",
        "procedural_capabilities",
        "facial_capabilities",
        "gaze_capabilities",
        "interaction_capabilities",
    ):
        values = getattr(profile, field)

        if (
            not isinstance(values, list)
            or not all(
                isinstance(value, str) and value.strip()
                for value in values
            )
        ):
            errors.append(
                f"Capability profile {field} must contain non-empty strings."
            )
        elif len(values) != len(set(values)):
            errors.append(
                f"Capability profile {field} must not contain duplicates."
            )

    return errors


def validate_animation_plan(
    actions: Iterable[CharacterActionSpec],
    animations: Iterable[CharacterAnimationSpec],
    capability_profiles: Iterable[CharacterCapabilityProfile] = (),
    registry=None,
) -> list[str]:
    """
    Validate action coverage, identity, timing, semantic definitions,
    and rig/executor capabilities.

    A custom semantic registry can be injected. If omitted, the default
    animation catalog is used.
    """
    action_list = list(actions)
    animation_list = list(animations)
    profile_list = list(capability_profiles)

    if registry is None:
        registry = build_default_catalog()

    errors: list[str] = []

    action_counts = Counter(action.id for action in action_list)
    animation_counts = Counter(
        animation.action_id for animation in animation_list
    )

    action_by_id = {action.id: action for action in action_list}
    profile_by_character = {
        profile.character_id: profile for profile in profile_list
    }

    for action_id, count in action_counts.items():
        if count > 1:
            errors.append(f"Duplicate source action ID '{action_id}'.")

    for action_id, count in animation_counts.items():
        if count > 1:
            errors.append(
                f"Multiple animation outputs reference action '{action_id}'."
            )
        if action_id not in action_by_id:
            errors.append(
                f"Animation references unknown action '{action_id}'."
            )

    for action in action_list:
        if animation_counts[action.id] == 0:
            errors.append(
                f"Missing animation output for action '{action.id}'."
            )

    seen_animation_ids: set[str] = set()

    for animation in animation_list:
        errors.extend(validate_animation_spec(animation))

        if animation.id in seen_animation_ids:
            errors.append(
                f"Duplicate animation specification ID '{animation.id}'."
            )
        seen_animation_ids.add(animation.id)

        action = action_by_id.get(animation.action_id)
        if action is None:
            continue

        if animation.character_id != action.character_id:
            errors.append(
                f"Animation '{animation.id}' character does not match "
                f"action '{action.id}'."
            )

        if animation.channel != action.channel:
            errors.append(
                f"Animation '{animation.id}' channel does not match "
                f"action '{action.id}'."
            )

        if (
            animation.start_frame != action.start_frame
            or animation.end_frame != action.end_frame
        ):
            errors.append(
                f"Animation '{animation.id}' timing does not match "
                f"action '{action.id}'."
            )

        if animation.transition_in and animation.transition_in.source_action_id:
            source = action_by_id.get(
                animation.transition_in.source_action_id
            )

            if source is None:
                errors.append(
                    f"Animation '{animation.id}' transition references "
                    "unknown source action."
                )
            elif (
                source.character_id != action.character_id
                or source.channel != action.channel
            ):
                errors.append(
                    f"Animation '{animation.id}' transition source must "
                    "use the same character and channel."
                )
            elif source.end_frame != action.start_frame:
                errors.append(
                    f"Animation '{animation.id}' transition source must "
                    "end when its action starts."
                )

        if animation.status == "unsupported" or animation.motion is None:
            continue

        motion = animation.motion
        semantic_id = motion.semantic_id

        try:
            definition = registry.get(semantic_id)
        except KeyError:
            errors.append(
                f"Unknown semantic animation '{semantic_id}'."
            )
            continue

        if motion.execution_mode not in definition.execution_modes:
            errors.append(
                f"Semantic animation '{semantic_id}' does not support "
                f"execution mode '{motion.execution_mode}'."
            )

        if animation.channel != definition.channel:
            errors.append(
                f"Semantic animation '{semantic_id}' belongs to channel "
                f"'{definition.channel}', not '{animation.channel}'."
            )

        profile = profile_by_character.get(animation.character_id)
        if profile is None:
            continue

        if animation.channel not in profile.supported_channels:
            errors.append(
                f"Character '{animation.character_id}' does not support "
                f"channel '{animation.channel}'."
            )

        required = set(definition.required_capabilities)
        supported = set(profile.supported_capabilities)
        missing_physical = required - supported

        for capability in sorted(missing_physical):
            errors.append(
                f"Character '{animation.character_id}' lacks required "
                f"physical capability '{capability}' for '{semantic_id}'."
            )

        if motion.execution_mode == "clip":
            if semantic_id not in profile.supported_semantic_ids:
                errors.append(
                    f"Character '{animation.character_id}' has no "
                    f"compatible clip for '{semantic_id}'."
                )

        elif motion.execution_mode == "procedural":
            procedural = set(profile.procedural_capabilities)
            missing_executor = required - procedural

            for capability in sorted(missing_executor):
                errors.append(
                    f"Character '{animation.character_id}' lacks "
                    f"procedural executor capability '{capability}' "
                    f"for '{semantic_id}'."
                )

    action_characters = {action.character_id for action in action_list}

    for profile in profile_list:
        errors.extend(validate_capability_profile(profile))

        if profile.character_id not in action_characters:
            errors.append(
                f"Capability profile references character "
                f"'{profile.character_id}' with no actions in this plan."
            )

    if len(profile_by_character) != len(profile_list):
        errors.append(
            "Duplicate capability profiles found for a character."
        )

    return errors
