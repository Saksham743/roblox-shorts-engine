
"""Tests for the renderer-independent SceneSpec contract."""

import pytest

from scripts.shorts.production.scene_spec import (
    AudioSpec,
    CharacterSpec,
    EnvironmentSpec,
    EventSpec,
    ProjectSpec,
    SceneSpec,
    SceneSpecification,
    ShotSpec,
    validate_scene_spec,
)


def make_valid_spec() -> SceneSpecification:
    """Create a valid 10-second town story for testing."""

    return SceneSpecification(
        project=ProjectSpec(
            title="A Normal Town",
            source_story=(
                "In this town everybody wakes up, do their work, "
                "and go to sleep, so I can say that everything "
                "in this town in normal"
            ),
            fps=30,
            width=1080,
            height=1920,
            duration_frames=300,
        ),
        characters=[
            CharacterSpec(
                id="citizen_01",
                name="Citizen 01",
                role="main_character",
                appearance="Blocky Roblox-style character",
                outfit="Blue shirt and black trousers",
            ),
            CharacterSpec(
                id="citizen_02",
                name="Citizen 02",
                role="background_citizen",
                appearance="Blocky Roblox-style character",
                outfit="Green shirt and brown trousers",
            ),
        ],
        environments=[
            EnvironmentSpec(
                id="town",
                name="Main Town",
                description="A small town with houses, roads and shops",
                environment_type="town",
                required_assets=["house", "road", "tree", "streetlight"],
            ),
        ],
        scenes=[
            SceneSpec(
                id="morning",
                name="Morning",
                description="The town wakes up",
                start_frame=0,
                end_frame=90,
                environment_id="town",
                time_of_day="morning",
                lighting_description="Warm sunrise lighting",
            ),
            SceneSpec(
                id="day",
                name="Day",
                description="Citizens go about their work",
                start_frame=90,
                end_frame=210,
                environment_id="town",
                time_of_day="day",
                lighting_description="Bright daylight",
            ),
            SceneSpec(
                id="night",
                name="Night",
                description="The town goes to sleep",
                start_frame=210,
                end_frame=300,
                environment_id="town",
                time_of_day="night",
                lighting_description="Dark blue sky and warm streetlights",
            ),
        ],
        events=[
            EventSpec(
                id="wake_up",
                scene_id="morning",
                name="Citizens wake up",
                description="Citizens leave their houses",
                start_frame=10,
                end_frame=80,
                action="walk",
                actor_ids=["citizen_01", "citizen_02"],
            ),
            EventSpec(
                id="work",
                scene_id="day",
                name="Citizens work",
                description="Citizens move through the town",
                start_frame=100,
                end_frame=200,
                action="walk",
                actor_ids=["citizen_01"],
            ),
            EventSpec(
                id="sleep",
                scene_id="night",
                name="Citizens return home",
                description="Citizens return to their houses",
                start_frame=220,
                end_frame=290,
                action="walk",
                actor_ids=["citizen_01", "citizen_02"],
            ),
        ],
        shots=[
            ShotSpec(
                id="morning_wide",
                scene_id="morning",
                start_frame=0,
                end_frame=90,
                subject_ids=[],
                framing="wide",
                angle="eye_level",
                movement="slow_push_in",
                camera_intent="Establish the town waking up",
            ),
            ShotSpec(
                id="day_tracking",
                scene_id="day",
                start_frame=90,
                end_frame=210,
                subject_ids=["citizen_01"],
                framing="medium",
                angle="eye_level",
                movement="tracking",
                camera_intent="Follow the main citizen",
            ),
            ShotSpec(
                id="night_pullback",
                scene_id="night",
                start_frame=210,
                end_frame=300,
                subject_ids=[],
                framing="wide",
                angle="eye_level",
                movement="slow_pull_back",
                camera_intent="Reveal the town settling down",
            ),
        ],
        audio=AudioSpec(
            narration_text="A normal day in a normal town.",
            music_description="Gentle music transitioning from day to night",
        ),
    )


def test_valid_specification_passes():
    spec = make_valid_spec()

    assert validate_scene_spec(spec) == []


def test_duplicate_character_ids_are_rejected():
    spec = make_valid_spec()
    spec.characters[1].id = "citizen_01"

    errors = validate_scene_spec(spec)

    assert any("duplicate ID" in error for error in errors)


def test_unknown_environment_is_rejected():
    spec = make_valid_spec()
    spec.scenes[0].environment_id = "missing_environment"

    errors = validate_scene_spec(spec)

    assert any("unknown environment" in error for error in errors)


def test_event_outside_parent_scene_is_rejected():
    spec = make_valid_spec()
    spec.events[0].start_frame = 85
    spec.events[0].end_frame = 95

    errors = validate_scene_spec(spec)

    assert any("falls outside scene" in error for error in errors)


def test_scene_timeline_gap_is_rejected():
    spec = make_valid_spec()
    spec.scenes[1].start_frame = 100

    errors = validate_scene_spec(spec)

    assert any("timeline gap" in error for error in errors)


def test_scene_overlap_is_rejected():
    spec = make_valid_spec()
    spec.scenes[1].start_frame = 80

    errors = validate_scene_spec(spec)

    assert any("overlap" in error for error in errors)


def test_unknown_shot_character_is_rejected():
    spec = make_valid_spec()
    spec.shots[1].subject_ids = ["missing_character"]

    errors = validate_scene_spec(spec)

    assert any("unknown character" in error for error in errors)


def test_shot_timeline_gap_is_rejected():
    spec = make_valid_spec()
    spec.shots[1].start_frame = 100

    errors = validate_scene_spec(spec)

    assert any("timeline gap" in error for error in errors)


def test_event_with_unknown_scene_is_rejected():
    spec = make_valid_spec()
    spec.events[0].scene_id = "missing_scene"

    errors = validate_scene_spec(spec)

    assert any("unknown scene" in error for error in errors)


def test_event_with_unknown_character_is_rejected():
    spec = make_valid_spec()
    spec.events[0].actor_ids = ["missing_character"]

    errors = validate_scene_spec(spec)

    assert any("unknown character" in error for error in errors)


def test_range_beyond_project_duration_is_rejected():
    spec = make_valid_spec()
    spec.events[0].end_frame = 350

    errors = validate_scene_spec(spec)

    assert any("exceeds project duration" in error for error in errors)


def test_empty_scenes_are_rejected():
    spec = make_valid_spec()
    spec.scenes = []

    errors = validate_scene_spec(spec)

    assert any("at least one scene" in error for error in errors)


def test_empty_shots_are_rejected():
    spec = make_valid_spec()
    spec.shots = []

    errors = validate_scene_spec(spec)

    assert any("at least one camera shot" in error for error in errors)


def test_shot_outside_parent_scene_is_rejected():
    spec = make_valid_spec()

    # Morning scene ends at frame 90.
    # This shot incorrectly continues into the day scene.
    spec.shots[0].end_frame = 100

    errors = validate_scene_spec(spec)

    assert any("falls outside scene 'morning'" in error for error in errors)


def test_shot_cannot_belong_to_an_unknown_scene():
    spec = make_valid_spec()
    spec.shots[0].scene_id = "missing_scene"

    errors = validate_scene_spec(spec)

    assert any("references unknown scene" in error for error in errors)



import json


def test_specification_to_dict():
    spec = make_valid_spec()

    data = spec.to_dict()

    assert data["project"]["title"] == "A Normal Town"
    assert data["scenes"][0]["id"] == "morning"
    assert data["characters"][0]["id"] == "citizen_01"


def test_specification_json_round_trip():
    spec = make_valid_spec()

    json_text = spec.to_json()
    loaded_spec = SceneSpecification.from_dict(json.loads(json_text))

    assert loaded_spec == spec
    assert validate_scene_spec(loaded_spec) == []


def test_save_and_load_json(tmp_path):
    spec = make_valid_spec()
    output_path = tmp_path / "production" / "scene_spec.json"

    saved_path = spec.save_json(output_path)

    assert saved_path.exists()

    loaded_spec = SceneSpecification.load_json(saved_path)

    assert loaded_spec == spec
    assert validate_scene_spec(loaded_spec) == []


def test_json_preserves_original_story_text():
    spec = make_valid_spec()
    original_story = spec.project.source_story

    json_text = spec.to_json()
    loaded_spec = SceneSpecification.from_dict(json.loads(json_text))

    assert loaded_spec.project.source_story == original_story


def test_from_dict_rejects_missing_required_fields():
    with pytest.raises(ValueError, match="Missing required"):
        SceneSpecification.from_dict({"project": {}})


def test_load_json_rejects_missing_file(tmp_path):
    missing_path = tmp_path / "missing_scene_spec.json"

    with pytest.raises(FileNotFoundError):
        SceneSpecification.load_json(missing_path)



def test_from_dict_rejects_non_list_scenes():
    spec = make_valid_spec()
    data = spec.to_dict()
    data["scenes"] = {"morning": {}}

    with pytest.raises(TypeError, match="'scenes' must be a list"):
        SceneSpecification.from_dict(data)


def test_from_dict_rejects_invalid_character_entry():
    spec = make_valid_spec()
    data = spec.to_dict()
    data["characters"][0] = "citizen_01"

    with pytest.raises(
        TypeError,
        match=r"'characters\[0\]' must be a dictionary",
    ):
        SceneSpecification.from_dict(data)


def test_from_dict_rejects_missing_character_fields():
    spec = make_valid_spec()
    data = spec.to_dict()
    del data["characters"][0]["outfit"]

    with pytest.raises(
        ValueError,
        match="Missing required fields in 'characters\\[0\\]'",
    ):
        SceneSpecification.from_dict(data)


def test_from_dict_rejects_unknown_character_fields():
    spec = make_valid_spec()
    data = spec.to_dict()
    data["characters"][0]["hair_color"] = "black"

    with pytest.raises(
        ValueError,
        match="Unknown fields in 'characters\\[0\\]'",
    ):
        SceneSpecification.from_dict(data)


def test_from_dict_rejects_unsupported_schema_version():
    spec = make_valid_spec()
    data = spec.to_dict()
    data["schema_version"] = "2.0.0"

    with pytest.raises(ValueError, match="Unsupported SceneSpec version"):
        SceneSpecification.from_dict(data)


def test_from_dict_rejects_invalid_sound_effect_entry():
    spec = make_valid_spec()
    data = spec.to_dict()
    data["audio"]["sound_effects"] = ["door_open"]

    with pytest.raises(
        TypeError,
        match=r"'audio.sound_effects\[0\]' must be a dictionary",
    ):
        SceneSpecification.from_dict(data)


def test_from_dict_rejects_string_fps():
    data = make_valid_spec().to_dict()
    data["project"]["fps"] = "30"

    with pytest.raises(TypeError, match="project.fps.*integer"):
        SceneSpecification.from_dict(data)


def test_from_dict_rejects_float_frame_number():
    data = make_valid_spec().to_dict()
    data["scenes"][0]["start_frame"] = 12.5

    with pytest.raises(TypeError, match=r"scenes\[0\]\.start_frame.*integer"):
        SceneSpecification.from_dict(data)


def test_from_dict_rejects_string_character_ids():
    data = make_valid_spec().to_dict()
    data["events"][0]["actor_ids"] = "citizen_01"

    with pytest.raises(TypeError, match=r"events\[0\]\.actor_ids.*list"):
        SceneSpecification.from_dict(data)


def test_from_dict_rejects_non_string_list_items():
    data = make_valid_spec().to_dict()
    data["events"][0]["actor_ids"] = [123]

    with pytest.raises(
        TypeError,
        match=r"events\[0\]\.actor_ids\[0\].*str",
    ):
        SceneSpecification.from_dict(data)


def test_from_dict_rejects_integer_title():
    data = make_valid_spec().to_dict()
    data["project"]["title"] = 123

    with pytest.raises(TypeError, match="project.title.*str"):
        SceneSpecification.from_dict(data)


def test_from_dict_rejects_boolean_fps():
    data = make_valid_spec().to_dict()
    data["project"]["fps"] = True

    with pytest.raises(TypeError, match="project.fps.*integer"):
        SceneSpecification.from_dict(data)


def test_empty_character_id_is_rejected():
    spec = make_valid_spec()
    spec.characters[0].id = ""

    errors = validate_scene_spec(spec)

    assert any(
        "Character must have a non-empty string ID" in error
        for error in errors
    )


def test_whitespace_character_id_is_rejected():
    spec = make_valid_spec()
    spec.characters[0].id = "   "

    errors = validate_scene_spec(spec)

    assert any(
        "Character must have a non-empty string ID" in error
        for error in errors
    )


def test_unsupported_camera_framing_is_rejected():
    spec = make_valid_spec()
    spec.shots[0].framing = "ultra_super_wide"

    errors = validate_scene_spec(spec)

    assert any("unsupported value" in error for error in errors)


def test_unsupported_camera_angle_is_rejected():
    spec = make_valid_spec()
    spec.shots[0].angle = "upside_down"

    errors = validate_scene_spec(spec)

    assert any("unsupported value" in error for error in errors)


def test_unsupported_camera_movement_is_rejected():
    spec = make_valid_spec()
    spec.shots[0].movement = "teleporting"

    errors = validate_scene_spec(spec)

    assert any("unsupported value" in error for error in errors)


def test_all_supported_camera_defaults_are_valid():
    spec = make_valid_spec()

    errors = validate_scene_spec(spec)

    assert not errors


def test_empty_character_name_is_rejected():
    spec = make_valid_spec()
    spec.characters[0].name = ""

    errors = validate_scene_spec(spec)

    assert any("name must be a non-empty string" in error for error in errors)


def test_empty_environment_description_is_rejected():
    spec = make_valid_spec()
    spec.environments[0].description = "   "

    errors = validate_scene_spec(spec)

    assert any("description must be a non-empty string" in error for error in errors)


def test_empty_event_action_is_rejected():
    spec = make_valid_spec()
    spec.events[0].action = ""

    errors = validate_scene_spec(spec)

    assert any("action must be a non-empty string" in error for error in errors)


def test_unsupported_time_of_day_is_rejected():
    spec = make_valid_spec()
    spec.scenes[0].time_of_day = "midnight_sunrise"

    errors = validate_scene_spec(spec)

    assert any("time_of_day has unsupported value" in error for error in errors)


def test_missing_time_of_day_is_allowed():
    spec = make_valid_spec()
    spec.scenes[0].time_of_day = None

    errors = validate_scene_spec(spec)

    assert not errors


def test_empty_project_visual_style_is_rejected():
    spec = make_valid_spec()
    spec.project.visual_style = ""

    errors = validate_scene_spec(spec)

    assert any("visual_style must be a non-empty string" in error for error in errors)


def test_valid_time_of_day_values_are_accepted():
    spec = make_valid_spec()

    valid_values = [
        "dawn",
        "morning",
        "day",
        "afternoon",
        "evening",
        "dusk",
        "night",
    ]

    for value in valid_values:
        spec.scenes[0].time_of_day = value
        assert validate_scene_spec(spec) == []
