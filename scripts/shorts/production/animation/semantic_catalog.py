
"""Default semantic animation vocabulary for the Roblox Shorts Engine."""

from __future__ import annotations

from .semantic_registry import (
    SemanticAnimationDefinition,
    SemanticAnimationRegistry,
)


def build_default_catalog() -> SemanticAnimationRegistry:
    """Build and return a fresh registry containing the default vocabulary."""

    definitions = [
        # ---------------------------------------------------------
        # LOCOMOTION
        # ---------------------------------------------------------
        SemanticAnimationDefinition(
            semantic_id="locomotion.idle",
            category="locomotion",
            channel="locomotion",
            description="Standing in a relaxed idle pose with subtle natural movement.",
            execution_modes=("clip", "procedural"),
            loopable=True,
            required_capabilities=("basic_locomotion",),
            tags=("idle", "standing", "rest", "neutral"),
        ),
        SemanticAnimationDefinition(
            semantic_id="locomotion.walk.relaxed",
            category="locomotion",
            channel="locomotion",
            description="Walking at a comfortable and casual pace.",
            execution_modes=("clip", "procedural"),
            loopable=True,
            required_capabilities=("basic_locomotion",),
            tags=("walking", "casual", "relaxed", "movement"),
        ),
        SemanticAnimationDefinition(
            semantic_id="locomotion.walk.brisk",
            category="locomotion",
            channel="locomotion",
            description="Walking with a purposeful and noticeably faster pace.",
            execution_modes=("clip", "procedural"),
            loopable=True,
            required_capabilities=("basic_locomotion",),
            tags=("walking", "brisk", "fast", "purposeful"),
        ),
        SemanticAnimationDefinition(
            semantic_id="locomotion.run",
            category="locomotion",
            channel="locomotion",
            description="Running with a faster and more energetic movement pattern.",
            execution_modes=("clip", "procedural"),
            loopable=True,
            required_capabilities=("basic_locomotion", "running"),
            tags=("running", "sprint", "fast", "movement"),
        ),
        SemanticAnimationDefinition(
            semantic_id="locomotion.jump",
            category="locomotion",
            channel="locomotion",
            description="Performing a jump and returning to a stable landing.",
            execution_modes=("clip", "procedural"),
            loopable=False,
            required_capabilities=("basic_locomotion", "jumping"),
            tags=("jump", "leap", "airborne", "landing"),
        ),

        # ---------------------------------------------------------
        # BODY
        # ---------------------------------------------------------
        SemanticAnimationDefinition(
            semantic_id="body.turn",
            category="body",
            channel="body",
            description="Turning the body towards a new direction or target.",
            execution_modes=("clip", "procedural"),
            loopable=False,
            required_capabilities=("body_control",),
            tags=("turn", "rotate", "orientation", "direction"),
        ),
        SemanticAnimationDefinition(
            semantic_id="body.lean",
            category="body",
            channel="body",
            description="Leaning the upper body in a particular direction.",
            execution_modes=("clip", "procedural"),
            loopable=False,
            required_capabilities=("body_control",),
            tags=("lean", "tilt", "posture", "balance"),
        ),
        SemanticAnimationDefinition(
            semantic_id="body.crouch",
            category="body",
            channel="body",
            description="Lowering the body into a crouched posture.",
            execution_modes=("clip", "procedural"),
            loopable=False,
            required_capabilities=("body_control", "lower_body_control"),
            tags=("crouch", "squat", "lower", "stealth"),
        ),

        # ---------------------------------------------------------
        # GESTURE
        # ---------------------------------------------------------
        SemanticAnimationDefinition(
            semantic_id="gesture.wave",
            category="gesture",
            channel="gesture",
            description="Waving a hand or arm to greet or acknowledge someone.",
            execution_modes=("clip", "procedural"),
            loopable=False,
            required_capabilities=("arm_gesture",),
            tags=("wave", "greeting", "hello", "acknowledgement"),
        ),
        SemanticAnimationDefinition(
            semantic_id="gesture.point",
            category="gesture",
            channel="gesture",
            description="Pointing towards a person, object, or direction.",
            execution_modes=("clip", "procedural"),
            loopable=False,
            required_capabilities=("arm_gesture",),
            tags=("point", "indicate", "direction", "attention"),
        ),
        SemanticAnimationDefinition(
            semantic_id="gesture.thumbs_up",
            category="gesture",
            channel="gesture",
            description="Raising a hand to communicate approval or encouragement.",
            execution_modes=("clip", "procedural"),
            loopable=False,
            required_capabilities=("arm_gesture", "hand_pose"),
            tags=("thumbs_up", "approval", "positive", "encouragement"),
        ),

        # ---------------------------------------------------------
        # FACIAL
        # ---------------------------------------------------------
        SemanticAnimationDefinition(
            semantic_id="facial.smile",
            category="facial",
            channel="facial",
            description="Displaying a friendly or happy smiling expression.",
            execution_modes=("clip", "procedural"),
            loopable=True,
            required_capabilities=("facial_expression",),
            tags=("smile", "happy", "friendly", "positive"),
        ),
        SemanticAnimationDefinition(
            semantic_id="facial.frown",
            category="facial",
            channel="facial",
            description="Displaying a sad, disappointed, or unhappy expression.",
            execution_modes=("clip", "procedural"),
            loopable=True,
            required_capabilities=("facial_expression",),
            tags=("frown", "sad", "disappointed", "negative"),
        ),
        SemanticAnimationDefinition(
            semantic_id="facial.surprised",
            category="facial",
            channel="facial",
            description="Displaying a surprised expression in response to an unexpected event.",
            execution_modes=("clip", "procedural"),
            loopable=False,
            required_capabilities=("facial_expression",),
            tags=("surprised", "shock", "unexpected", "reaction"),
        ),

        # ---------------------------------------------------------
        # GAZE
        # ---------------------------------------------------------
        SemanticAnimationDefinition(
            semantic_id="gaze.look_at",
            category="gaze",
            channel="gaze",
            description="Directing visual attention towards a specified target.",
            execution_modes=("clip", "procedural"),
            loopable=True,
            required_capabilities=("gaze_control",),
            tags=("look_at", "focus", "attention", "target"),
        ),
        SemanticAnimationDefinition(
            semantic_id="gaze.look_away",
            category="gaze",
            channel="gaze",
            description="Redirecting visual attention away from the current target.",
            execution_modes=("clip", "procedural"),
            loopable=False,
            required_capabilities=("gaze_control",),
            tags=("look_away", "avert", "avoid", "attention"),
        ),

        # ---------------------------------------------------------
        # INTERACTION
        # ---------------------------------------------------------
        SemanticAnimationDefinition(
            semantic_id="interaction.handshake",
            category="interaction",
            channel="interaction",
            description="Performing a handshake with another character.",
            execution_modes=("clip", "procedural"),
            loopable=False,
            required_capabilities=("arm_gesture", "character_interaction"),
            tags=("handshake", "greeting", "social", "cooperation"),
        ),
        SemanticAnimationDefinition(
            semantic_id="interaction.hug",
            category="interaction",
            channel="interaction",
            description="Performing a friendly or affectionate hug with another character.",
            execution_modes=("clip", "procedural"),
            loopable=False,
            required_capabilities=("arm_gesture", "character_interaction"),
            tags=("hug", "embrace", "social", "affection"),
        ),
        SemanticAnimationDefinition(
            semantic_id="interaction.high_five",
            category="interaction",
            channel="interaction",
            description="Performing a high five with another character.",
            execution_modes=("clip", "procedural"),
            loopable=False,
            required_capabilities=("arm_gesture", "character_interaction"),
            tags=("high_five", "celebration", "social", "greeting"),
        ),

        # ---------------------------------------------------------
        # PROP
        # ---------------------------------------------------------
        SemanticAnimationDefinition(
            semantic_id="prop.pick_up",
            category="prop",
            channel="prop",
            description="Reaching for and picking up an object.",
            execution_modes=("clip", "procedural"),
            loopable=False,
            required_capabilities=("arm_gesture", "prop_interaction"),
            tags=("pickup", "grab", "collect", "object"),
        ),
        SemanticAnimationDefinition(
            semantic_id="prop.hold",
            category="prop",
            channel="prop",
            description="Maintaining a holding pose while carrying an object.",
            execution_modes=("clip", "procedural"),
            loopable=True,
            required_capabilities=("arm_gesture", "prop_interaction"),
            tags=("hold", "carry", "object", "pose"),
        ),
        SemanticAnimationDefinition(
            semantic_id="prop.put_down",
            category="prop",
            channel="prop",
            description="Lowering and releasing an object into a resting position.",
            execution_modes=("clip", "procedural"),
            loopable=False,
            required_capabilities=("arm_gesture", "prop_interaction"),
            tags=("put_down", "release", "place", "object"),
        ),
    ]

    registry = SemanticAnimationRegistry()

    for definition in definitions:
        registry.register(definition)

    return registry
