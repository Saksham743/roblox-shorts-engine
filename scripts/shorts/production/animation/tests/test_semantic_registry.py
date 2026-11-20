
import pytest

from scripts.shorts.production.animation.semantic_registry import (
    SemanticAnimationDefinition,
    SemanticAnimationRegistry,
)


VALID_CHANNELS = {
    "locomotion",
    "body",
    "gesture",
    "facial",
    "gaze",
    "interaction",
    "prop",
}


def make_definition(**overrides):
    values = {
        "semantic_id": "locomotion.walk.relaxed",
        "category": "locomotion",
        "channel": "locomotion",
        "description": "Casual walking at a relaxed pace.",
        "execution_modes": ("clip", "procedural"),
        "loopable": True,
        "required_capabilities": ("basic_locomotion",),
        "tags": ("walking", "casual", "movement"),
    }
    values.update(overrides)
    return SemanticAnimationDefinition(**values)


def test_register_and_retrieve_definition():
    registry = SemanticAnimationRegistry()
    definition = make_definition()

    registry.register(definition)

    assert registry.get("locomotion.walk.relaxed") == definition


def test_register_rejects_duplicate_semantic_ids():
    registry = SemanticAnimationRegistry()

    registry.register(make_definition())

    with pytest.raises(ValueError, match="already registered"):
        registry.register(make_definition())


def test_retrieve_unknown_semantic_id_raises_key_error():
    registry = SemanticAnimationRegistry()

    with pytest.raises(KeyError, match="unknown.semantic"):
        registry.get("unknown.semantic")


@pytest.mark.parametrize(
    "channel",
    sorted(VALID_CHANNELS),
)
def test_all_supported_channels_are_accepted(channel):
    registry = SemanticAnimationRegistry()
    definition = make_definition(
        semantic_id=f"test.{channel}",
        category="test",
        channel=channel,
    )

    registry.register(definition)

    assert registry.get(f"test.{channel}").channel == channel


def test_invalid_channel_is_rejected():
    with pytest.raises(ValueError, match="channel"):
        make_definition(channel="invalid_channel")


def test_invalid_execution_mode_is_rejected():
    with pytest.raises(ValueError, match="execution"):
        make_definition(execution_modes=("clip", "teleport"))


def test_empty_execution_modes_are_rejected():
    with pytest.raises(ValueError, match="execution"):
        make_definition(execution_modes=())


def test_invalid_semantic_id_is_rejected():
    with pytest.raises(ValueError, match="semantic"):
        make_definition(semantic_id="Walk Relaxed")


def test_empty_description_is_rejected():
    with pytest.raises(ValueError, match="description"):
        make_definition(description="  ")


def test_get_by_channel_returns_matching_definitions():
    registry = SemanticAnimationRegistry()

    walking = make_definition()
    waving = make_definition(
        semantic_id="gesture.wave",
        category="gesture",
        channel="gesture",
        description="Waving to greet someone.",
        execution_modes=("clip",),
        loopable=False,
        required_capabilities=("arm_gesture",),
        tags=("wave", "greeting"),
    )

    registry.register(walking)
    registry.register(waving)

    results = registry.get_by_channel("gesture")

    assert len(results) == 1
    assert results[0].semantic_id == "gesture.wave"


def test_search_by_tags_returns_matching_definitions():
    registry = SemanticAnimationRegistry()

    registry.register(make_definition())
    registry.register(
        make_definition(
            semantic_id="locomotion.run",
            description="Running at a fast pace.",
            tags=("running", "fast", "movement"),
        )
    )

    results = registry.search_by_tags({"movement"})

    assert len(results) == 2


def test_search_by_multiple_tags_uses_any_match():
    registry = SemanticAnimationRegistry()
    registry.register(make_definition())

    results = registry.search_by_tags({"walking", "greeting"})

    assert len(results) == 1


def test_registry_returns_all_registered_definitions():
    registry = SemanticAnimationRegistry()

    registry.register(make_definition())
    registry.register(
        make_definition(
            semantic_id="gesture.wave",
            category="gesture",
            channel="gesture",
            description="Waving to greet someone.",
            execution_modes=("clip",),
            loopable=False,
            required_capabilities=("arm_gesture",),
            tags=("wave", "greeting"),
        )
    )

    assert len(registry.all()) == 2


def test_definition_is_immutable():
    definition = make_definition()

    with pytest.raises(AttributeError):
        definition.semantic_id = "locomotion.run"


def test_definition_uses_immutable_collections():
    definition = make_definition()

    assert isinstance(definition.execution_modes, tuple)
    assert isinstance(definition.required_capabilities, tuple)
    assert isinstance(definition.tags, tuple)


def test_registry_does_not_allow_duplicate_tags_to_affect_search():
    registry = SemanticAnimationRegistry()

    registry.register(
        make_definition(tags=("walking", "walking", "movement"))
    )

    results = registry.search_by_tags({"walking"})

    assert len(results) == 1
