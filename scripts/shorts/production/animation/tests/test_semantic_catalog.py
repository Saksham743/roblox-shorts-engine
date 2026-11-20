
import pytest

from scripts.shorts.production.animation.semantic_catalog import (
    build_default_catalog,
)


EXPECTED_SEMANTIC_IDS = {
    "locomotion.idle",
    "locomotion.walk.relaxed",
    "locomotion.walk.brisk",
    "locomotion.run",
    "locomotion.jump",
    "body.turn",
    "body.lean",
    "body.crouch",
    "gesture.wave",
    "gesture.point",
    "gesture.thumbs_up",
    "facial.smile",
    "facial.frown",
    "facial.surprised",
    "gaze.look_at",
    "gaze.look_away",
    "interaction.handshake",
    "interaction.hug",
    "interaction.high_five",
    "prop.pick_up",
    "prop.hold",
    "prop.put_down",
}


def test_default_catalog_contains_all_expected_definitions():
    catalog = build_default_catalog()

    actual_ids = {
        definition.semantic_id
        for definition in catalog.all()
    }

    assert actual_ids == EXPECTED_SEMANTIC_IDS


def test_default_catalog_has_no_duplicate_definitions():
    catalog = build_default_catalog()

    semantic_ids = [
        definition.semantic_id
        for definition in catalog.all()
    ]

    assert len(semantic_ids) == len(set(semantic_ids))


def test_default_catalog_covers_all_seven_channels():
    catalog = build_default_catalog()

    actual_channels = {
        definition.channel
        for definition in catalog.all()
    }

    assert actual_channels == {
        "locomotion",
        "body",
        "gesture",
        "facial",
        "gaze",
        "interaction",
        "prop",
    }


@pytest.mark.parametrize(
    ("semantic_id", "expected_channel"),
    [
        ("locomotion.walk.relaxed", "locomotion"),
        ("body.turn", "body"),
        ("gesture.wave", "gesture"),
        ("facial.smile", "facial"),
        ("gaze.look_at", "gaze"),
        ("interaction.handshake", "interaction"),
        ("prop.pick_up", "prop"),
    ],
)
def test_semantic_definitions_use_correct_channels(
    semantic_id,
    expected_channel,
):
    catalog = build_default_catalog()

    definition = catalog.get(semantic_id)

    assert definition.channel == expected_channel


def test_walk_supports_clip_and_procedural_execution():
    catalog = build_default_catalog()

    definition = catalog.get("locomotion.walk.relaxed")

    assert set(definition.execution_modes) == {
        "clip",
        "procedural",
    }


def test_loopable_actions_are_marked_correctly():
    catalog = build_default_catalog()

    assert catalog.get("locomotion.idle").loopable is True
    assert catalog.get("locomotion.walk.relaxed").loopable is True
    assert catalog.get("locomotion.run").loopable is True

    assert catalog.get("gesture.wave").loopable is False
    assert catalog.get("prop.pick_up").loopable is False


def test_definitions_have_required_capabilities():
    catalog = build_default_catalog()

    for definition in catalog.all():
        assert isinstance(definition.required_capabilities, tuple)
        assert all(
            isinstance(capability, str) and capability.strip()
            for capability in definition.required_capabilities
        )


def test_definitions_have_searchable_tags():
    catalog = build_default_catalog()

    for definition in catalog.all():
        assert isinstance(definition.tags, tuple)
        assert len(definition.tags) > 0


def test_each_catalog_build_returns_an_independent_registry():
    first_catalog = build_default_catalog()
    second_catalog = build_default_catalog()

    first_catalog.register(
        type(first_catalog.all()[0])(
            semantic_id="custom.test",
            category="custom",
            channel="body",
            description="A custom test action.",
            execution_modes=("procedural",),
            loopable=False,
            required_capabilities=("body_control",),
            tags=("custom", "test"),
        )
    )

    assert "custom.test" in first_catalog
    assert "custom.test" not in second_catalog


def test_catalog_definitions_are_immutable():
    catalog = build_default_catalog()

    definition = catalog.get("gesture.wave")

    with pytest.raises(AttributeError):
        definition.semantic_id = "gesture.dance"
