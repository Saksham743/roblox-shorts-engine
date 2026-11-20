import json

import pytest

from scripts.shorts.production.animation import (
    AnimationIssueSpec,
    AnimationMotionSpec,
    AnimationPerformanceSpec,
    AnimationTransitionSpec,
    CharacterAnimationSpec,
    CharacterCapabilityProfile,
    validate_animation_plan,
    validate_animation_spec,
)
from scripts.shorts.production.scene_spec import CharacterActionSpec

from scripts.shorts.production.animation.semantic_catalog import build_default_catalog


def make_action(**overrides):
    values = dict(
        id="action_walk", scene_id="scene_1", character_id="char_1",
        action="walk", channel="locomotion", description="Walk to the shop.",
        start_frame=0, end_frame=60,
    )
    values.update(overrides)
    return CharacterActionSpec(**values)


def make_animation(**overrides):
    values = dict(
        id="animation_walk", action_id="action_walk", character_id="char_1",
        channel="locomotion", start_frame=0, end_frame=60, status="supported",
        motion=AnimationMotionSpec(
            semantic_id="locomotion.walk.relaxed", execution_mode="clip",
            description="Walk naturally.", loop=True,
        ),
        performance=AnimationPerformanceSpec(
            energy="medium", speed="normal", weight="normal", intensity="subtle",
            emotion="relaxed",
        ),
    )
    values.update(overrides)
    return CharacterAnimationSpec(**values)


def make_profile(**overrides):
    values = dict(
        character_id="char_1",
        rig_type="R15",
        supported_channels=["locomotion"],
        supported_semantic_ids=["locomotion.walk.relaxed"],
        supported_capabilities=["basic_locomotion"],
        procedural_capabilities=["basic_locomotion"],
    )
    values.update(overrides)
    return CharacterCapabilityProfile(**values)


def test_animation_spec_can_be_created():
    assert make_animation().action_id == "action_walk"


def test_animation_spec_serializes_nested_models():
    data = make_animation().to_dict()
    assert data["motion"]["semantic_id"] == "locomotion.walk.relaxed"
    assert data["performance"]["energy"] == "medium"


def test_animation_spec_json_round_trip():
    original = make_animation(
        transition_in=AnimationTransitionSpec(source_action_id="action_idle"),
        issues=[AnimationIssueSpec(code="NOTE", message="Using a reusable clip.")],
    )
    restored = CharacterAnimationSpec.from_json(original.to_json())
    assert restored == original


def test_animation_spec_save_and_load_json(tmp_path):
    original = make_animation()
    path = original.save_json(tmp_path / "nested" / "animation.json")
    assert CharacterAnimationSpec.load_json(path) == original


def test_from_dict_rejects_unknown_top_level_field():
    data = make_animation().to_dict()
    data["blender_bones"] = []
    with pytest.raises(ValueError, match="Unknown CharacterAnimationSpec fields"):
        CharacterAnimationSpec.from_dict(data)


def test_from_dict_rejects_missing_required_field():
    data = make_animation().to_dict()
    del data["action_id"]
    with pytest.raises(ValueError, match="Missing CharacterAnimationSpec fields"):
        CharacterAnimationSpec.from_dict(data)


def test_from_dict_rejects_invalid_nested_motion():
    data = make_animation().to_dict()
    data["motion"] = "walk"
    with pytest.raises(TypeError, match="motion.*dictionary"):
        CharacterAnimationSpec.from_dict(data)


def test_from_dict_rejects_unknown_nested_field():
    data = make_animation().to_dict()
    data["motion"]["bone_name"] = "LeftArm"
    with pytest.raises(ValueError, match="Unknown fields in 'motion'"):
        CharacterAnimationSpec.from_dict(data)


def test_clip_and_procedural_execution_modes_are_supported():
    assert validate_animation_spec(make_animation()) == []
    procedural = make_animation(motion=AnimationMotionSpec(
        semantic_id="locomotion.walk.relaxed", execution_mode="procedural",
        description="Generate a relaxed walk.",
    ))
    assert validate_animation_spec(procedural) == []


def test_unsupported_output_has_no_motion_or_performance():
    spec = make_animation(
        status="unsupported", motion=None, performance=None,
        issues=[AnimationIssueSpec(code="MISSING_RIG", message="No facial rig is available.")],
    )
    assert validate_animation_spec(spec) == []


def test_unsupported_output_requires_issue():
    spec = make_animation(status="unsupported", motion=None, performance=None)
    assert any("at least one issue" in error for error in validate_animation_spec(spec))


def test_unsupported_output_rejects_motion_instructions():
    spec = make_animation(status="unsupported", issues=[AnimationIssueSpec(code="X", message="Unavailable")])
    assert any("must not contain motion" in error for error in validate_animation_spec(spec))


def test_degraded_output_requires_documented_fallback():
    spec = make_animation(status="degraded", issues=[AnimationIssueSpec(code="FALLBACK", message="Simplified.")])
    assert any("document its fallback" in error for error in validate_animation_spec(spec))


def test_degraded_output_accepts_documented_fallback():
    spec = make_animation(status="degraded", issues=[AnimationIssueSpec(
        code="FALLBACK", message="No facial rig.", fallback_description="Use a head tilt instead."
    )])
    assert validate_animation_spec(spec) == []


def test_invalid_motion_mode_is_rejected():
    spec = make_animation(motion=AnimationMotionSpec("walk", "magic", "Walk."))
    assert any("execution_mode" in error for error in validate_animation_spec(spec))


def test_invalid_performance_vocabulary_is_rejected():
    spec = make_animation(performance=AnimationPerformanceSpec("extreme", "normal", "normal", "subtle"))
    assert any("performance energy" in error for error in validate_animation_spec(spec))


def test_invalid_transition_is_rejected():
    spec = make_animation(transition_in=AnimationTransitionSpec(duration_frames=-1, style="teleport"))
    errors = validate_animation_spec(spec)
    assert any("duration_frames" in error for error in errors)
    assert any("transition style" in error for error in errors)


def test_motion_parameters_must_be_scalar_values():
    spec = make_animation(motion=AnimationMotionSpec(
        "locomotion.walk.relaxed", "clip", "Walk.", parameters={"bad": [1, 2]}
    ))
    assert any("scalar value" in error for error in validate_animation_spec(spec))


def test_capability_profile_round_trip():
    profile = make_profile(facial_capabilities=["facial.smile"], gaze_capabilities=["gaze.head"])
    assert CharacterCapabilityProfile.from_json(profile.to_json()) == profile


def test_capability_profile_rejects_non_string_list_item():
    with pytest.raises(TypeError, match="list of strings"):
        CharacterCapabilityProfile.from_dict({"character_id": "char_1", "rig_type": "R15", "supported_channels": [1]})


def test_capability_profile_rejects_unknown_field():
    with pytest.raises(ValueError, match="Unknown CharacterCapabilityProfile fields"):
        CharacterCapabilityProfile.from_dict({"character_id": "char_1", "rig_type": "R15", "bone_names": []})


def test_capability_profile_validation_rejects_duplicates():
    profile = make_profile(supported_channels=["locomotion", "locomotion"])
    from scripts.shorts.production.animation import validate_capability_profile
    assert any("duplicates" in error for error in validate_capability_profile(profile))

def test_capability_profile_validation_checks_supported_capabilities():
    from scripts.shorts.production.animation import validate_capability_profile

    profile = make_profile(
        supported_capabilities=["basic_locomotion", "basic_locomotion"]
    )

    assert any(
        "supported_capabilities" in error and "duplicates" in error
        for error in validate_capability_profile(profile)
    )


def test_clip_requires_physical_rig_capabilities():
    profile = make_profile(supported_capabilities=[])

    errors = validate_animation_plan(
        [make_action()],
        [make_animation()],
        [profile],
    )

    assert any("basic_locomotion" in error for error in errors)


def test_procedural_motion_requires_physical_rig_capabilities():
    animation = make_animation(
        motion=AnimationMotionSpec(
            "locomotion.walk.relaxed",
            "procedural",
            "Generate a relaxed walk.",
        )
    )

    profile = make_profile(supported_capabilities=[])

    errors = validate_animation_plan(
        [make_action()],
        [animation],
        [profile],
    )

    assert any("basic_locomotion" in error for error in errors)


def test_procedural_motion_requires_executor_capabilities():
    animation = make_animation(
        motion=AnimationMotionSpec(
            "locomotion.walk.relaxed",
            "procedural",
            "Generate a relaxed walk.",
        )
    )

    profile = make_profile(procedural_capabilities=[])

    errors = validate_animation_plan(
        [make_action()],
        [animation],
        [profile],
    )

    assert any("procedural" in error.lower() for error in errors)


def test_clip_does_not_require_procedural_executor():
    profile = make_profile(procedural_capabilities=[])

    assert validate_animation_plan(
        [make_action()],
        [make_animation()],
        [profile],
    ) == []


def test_unknown_semantic_animation_is_rejected():
    animation = make_animation(
        motion=AnimationMotionSpec(
            "locomotion.teleport",
            "clip",
            "Teleport instantly.",
        )
    )

    errors = validate_animation_plan(
        [make_action()],
        [animation],
        [make_profile()],
    )

    assert any("unknown semantic" in error.lower() for error in errors)


def test_default_catalog_can_be_supplied_to_animation_plan():
    animation = make_animation(
        motion=AnimationMotionSpec(
            "locomotion.walk.relaxed",
            "clip",
            "Walk naturally.",
        )
    )

    assert validate_animation_plan(
        [make_action()],
        [animation],
        [make_profile()],
        registry=build_default_catalog(),
    ) == []

def test_plan_requires_one_output_per_action():
    errors = validate_animation_plan([make_action()], [])
    assert any("Missing animation output" in error for error in errors)


def test_plan_rejects_multiple_outputs_for_one_action():
    first = make_animation()
    second = make_animation(id="animation_walk_2")
    errors = validate_animation_plan([make_action()], [first, second])
    assert any("Multiple animation outputs" in error for error in errors)


def test_plan_rejects_animation_for_unknown_action():
    errors = validate_animation_plan([], [make_animation()])
    assert any("unknown action" in error for error in errors)


def test_plan_requires_matching_character_channel_and_timing():
    action = make_action()
    animation = make_animation(character_id="other", channel="body", start_frame=1, end_frame=59)
    errors = validate_animation_plan([action], [animation])
    assert any("character does not match" in error for error in errors)
    assert any("channel does not match" in error for error in errors)
    assert any("timing does not match" in error for error in errors)


def test_plan_accepts_clip_supported_by_profile():
    assert validate_animation_plan([make_action()], [make_animation()], [make_profile()]) == []


def test_plan_rejects_clip_missing_from_profile():
    profile = make_profile(supported_semantic_ids=[])
    errors = validate_animation_plan([make_action()], [make_animation()], [profile])
    assert any("no compatible clip" in error for error in errors)


def test_plan_rejects_missing_procedural_capability():
    animation = make_animation(motion=AnimationMotionSpec(
        "locomotion.walk.relaxed", "procedural", "Generate a walk."
    ))
    profile = make_profile(procedural_capabilities=[])
    errors = validate_animation_plan([make_action()], [animation], [profile])
    assert any("procedural" in error.lower() for error in errors)


def test_plan_rejects_unsupported_channel_from_profile():
    profile = make_profile(supported_channels=[])
    errors = validate_animation_plan([make_action()], [make_animation()], [profile])
    assert any("does not support channel" in error for error in errors)


def test_transition_source_must_exist_and_match_character_channel_and_timing():
    previous = make_action(id="action_previous", start_frame=0, end_frame=30)
    current = make_action(id="action_current", start_frame=30, end_frame=60)
    animation = make_animation(action_id="action_current", start_frame=30, end_frame=60,
        transition_in=AnimationTransitionSpec(source_action_id="action_previous"))
    assert validate_animation_plan([previous, current], [make_animation(id="animation_previous", action_id="action_previous", end_frame=30), animation]) == []


def test_transition_rejects_unknown_source_action():
    animation = make_animation(transition_in=AnimationTransitionSpec(source_action_id="missing"))
    errors = validate_animation_plan([make_action()], [animation])
    assert any("unknown source action" in error for error in errors)


def test_transition_rejects_wrong_character():
    previous = make_action(id="previous", character_id="other_character", end_frame=30)
    current = make_action(id="current", start_frame=30, end_frame=60)
    previous_animation = make_animation(action_id="previous", end_frame=30)
    current_animation = make_animation(action_id="current", start_frame=30, end_frame=60,
        transition_in=AnimationTransitionSpec(source_action_id="previous"))
    errors = validate_animation_plan([previous, current], [previous_animation, current_animation])
    assert any("same character and channel" in error for error in errors)


def test_plan_allows_multiple_channels_for_same_character():
    locomotion = make_action(id="walk", channel="locomotion")
    facial = make_action(id="talk", action="talk", channel="facial")
    walk_animation = make_animation(action_id="walk")
    talk_animation = make_animation(id="animation_talk", action_id="talk", channel="facial", motion=AnimationMotionSpec("facial.smile", "clip", "Smile."))
    profile = make_profile(
            supported_channels=["locomotion", "facial"],
            supported_semantic_ids=[
                "locomotion.walk.relaxed",
                "facial.smile",
            ],
            supported_capabilities=[
                "basic_locomotion",
                "facial_expression",
            ],
        )
    assert validate_animation_plan([locomotion, facial], [walk_animation, talk_animation], [profile]) == []
