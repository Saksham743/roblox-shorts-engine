
"""Configuration and executable discovery for the Blender rendering backend."""

from __future__ import annotations

import os
from pathlib import Path


# Project root:
# E:\roblox engine
PROJECT_ROOT = Path(__file__).resolve().parents[3]


# Default Blender installation on this machine.
DEFAULT_BLENDER_PATH = Path(r"E:\Blender 5.3\blender.exe")


def get_blender_executable() -> Path:
    """
    Resolve the Blender executable.

    Priority:
    1. BLENDER_EXECUTABLE environment variable.
    2. Default installation path.
    """

    configured_path = os.environ.get("BLENDER_EXECUTABLE")

    if configured_path:
        blender_path = Path(configured_path).expanduser()
    else:
        blender_path = DEFAULT_BLENDER_PATH

    blender_path = blender_path.resolve()

    if not blender_path.is_file():
        raise FileNotFoundError(
            f"Blender executable not found: {blender_path}\n"
            "Install Blender or set the BLENDER_EXECUTABLE environment variable."
        )

    return blender_path


def get_blender_version_command() -> list[str]:
    """Return the command used to inspect the Blender installation."""

    executable = get_blender_executable()

    return [
        str(executable),
        "--version",
    ]
