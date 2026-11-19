
"""Subprocess runner for Blender background operations."""

from __future__ import annotations

import subprocess
from pathlib import Path

from .config import get_blender_executable


def run_blender(
    arguments: list[str],
    timeout: int = 120,
) -> subprocess.CompletedProcess:
    """
    Run Blender in a separate process.

    Args:
        arguments: Arguments passed to Blender.
        timeout: Maximum execution time in seconds.

    Returns:
        CompletedProcess containing stdout, stderr and return code.

    Raises:
        subprocess.TimeoutExpired: If Blender exceeds the timeout.
        subprocess.CalledProcessError: If Blender exits unsuccessfully.
    """

    executable = get_blender_executable()

    command = [str(executable), *arguments]

    print("Launching Blender:")
    print(" ".join(f'"{part}"' if " " in part else part for part in command))

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )

    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode,
            command,
            output=result.stdout,
            stderr=result.stderr,
        )

    return result


def get_blender_version() -> str:
    """Launch Blender and return its version information."""

    result = run_blender(["--version"])

    return result.stdout.strip().splitlines()[0]
