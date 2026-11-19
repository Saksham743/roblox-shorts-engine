
"""Worker dispatcher for executing Python scripts inside Blender."""

from __future__ import annotations

import subprocess
from pathlib import Path

from .config import PROJECT_ROOT
from .runner import run_blender


def execute_worker(
    script_path: str | Path,
    script_args: list[str] | None = None,
    timeout: int = 120,
) -> subprocess.CompletedProcess:
    """
    Execute a Python script inside Blender.

    Args:
        script_path: Path to the Blender-side Python script.
        script_args: Optional arguments passed to that script.
        timeout: Maximum execution time in seconds.

    Returns:
        CompletedProcess containing Blender's output and return code.

    Raises:
        FileNotFoundError: If the worker script does not exist.
        ValueError: If the timeout is invalid.
        subprocess.TimeoutExpired: If Blender exceeds the timeout.
        subprocess.CalledProcessError: If Blender exits unsuccessfully.
    """

    if timeout <= 0:
        raise ValueError("Timeout must be greater than zero.")

    script_path = Path(script_path)

    # Resolve relative paths from the project root.
    if not script_path.is_absolute():
        script_path = PROJECT_ROOT / script_path

    script_path = script_path.resolve()

    if not script_path.is_file():
        raise FileNotFoundError(
            f"Blender worker script not found: {script_path}"
        )

    arguments = [
        "--background",
        "--factory-startup",
        "--python",
        str(script_path),
        "--",
        *(script_args or []),
    ]

    print(f"Executing Blender worker: {script_path}")

    result = run_blender(
        arguments,
        timeout=timeout,
    )

    return result
