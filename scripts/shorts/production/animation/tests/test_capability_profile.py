
import pytest

from scripts.shorts.production.animation.capability_profile import (
    CharacterCapabilityProfile,
)


def test_profile_accepts_supported_capabilities():
    profile = CharacterCapabilityProfile(
        character_id="character_01",
        rig_type="roblox_r15",
        supported_capabilities=[
            "basic_locomotion",
            "body_control",
            "arm_gesture",
        ],
    )

    assert profile.supported_capabilities == [
        "basic_locomotion",
        "body_control",
        "arm_gesture",
    ]


def test_profile_serializes_supported_capabilities():
    profile = CharacterCapabilityProfile(
        character_id="character_01",
        rig_type="roblox_r15",
        supported_capabilities=["basic_locomotion"],
    )

    data = profile.to_dict()

    assert data["supported_capabilities"] == ["basic_locomotion"]


def test_profile_json_round_trip_preserves_supported_capabilities():
    profile = CharacterCapabilityProfile(
        character_id="character_01",
        rig_type="roblox_r15",
        supported_capabilities=[
            "basic_locomotion",
            "facial_expression",
        ],
    )

    restored = CharacterCapabilityProfile.from_json(profile.to_json())

    assert restored == profile


def test_legacy_profile_without_supported_capabilities_still_loads():
    legacy_data = {
        "character_id": "character_01",
        "rig_type": "roblox_r15",
        "supported_channels": ["locomotion"],
        "supported_semantic_ids": ["locomotion.walk.relaxed"],
        "procedural_capabilities": ["basic_locomotion"],
        "facial_capabilities": [],
        "gaze_capabilities": [],
        "interaction_capabilities": [],
    }

    profile = CharacterCapabilityProfile.from_dict(legacy_data)

    assert profile.supported_capabilities == []
    assert profile.character_id == "character_01"


def test_profile_rejects_non_string_supported_capability():
    with pytest.raises(TypeError):
        CharacterCapabilityProfile.from_dict({
            "character_id": "character_01",
            "rig_type": "roblox_r15",
            "supported_capabilities": ["basic_locomotion", 123],
        })


def test_profile_rejects_non_list_supported_capabilities():
    with pytest.raises(TypeError):
        CharacterCapabilityProfile.from_dict({
            "character_id": "character_01",
            "rig_type": "roblox_r15",
            "supported_capabilities": "basic_locomotion",
        })


def test_profile_defaults_all_optional_capability_lists():
    profile = CharacterCapabilityProfile.from_dict({
        "character_id": "character_01",
        "rig_type": "roblox_r15",
    })

    assert profile.supported_channels == []
    assert profile.supported_semantic_ids == []
    assert profile.supported_capabilities == []
    assert profile.procedural_capabilities == []
