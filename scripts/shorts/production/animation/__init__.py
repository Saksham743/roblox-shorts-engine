"""Animation Director data contracts and validation."""

from .animation_spec import (
    AnimationIssueSpec,
    AnimationMotionSpec,
    AnimationPerformanceSpec,
    AnimationTransitionSpec,
    CharacterAnimationSpec,
)
from .capability_profile import CharacterCapabilityProfile
from .validation import (
    validate_animation_plan,
    validate_animation_spec,
    validate_capability_profile,
)

__all__ = [
    "AnimationIssueSpec",
    "AnimationMotionSpec",
    "AnimationPerformanceSpec",
    "AnimationTransitionSpec",
    "CharacterAnimationSpec",
    "CharacterCapabilityProfile",
    "validate_animation_plan",
    "validate_animation_spec",
    "validate_capability_profile",
]
