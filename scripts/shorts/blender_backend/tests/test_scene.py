
"""Blender integration smoke test.

Creates a cube, camera and light, then renders one PNG.
This script must execute inside Blender.
"""

from __future__ import annotations

import sys
from pathlib import Path

import bpy


def get_output_path() -> Path:
    """Read the output PNG path passed after Blender's -- separator."""

    args = sys.argv

    if "--" not in args:
        raise RuntimeError("Missing arguments after Blender's -- separator.")

    worker_args = args[args.index("--") + 1:]

    if len(worker_args) != 1:
        raise RuntimeError("Expected exactly one output PNG path.")

    return Path(worker_args[0]).expanduser().resolve()


def build_test_scene() -> None:
    """Build a simple scene to verify Blender's rendering pipeline."""

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    # Create cube
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    cube = bpy.context.object
    cube.name = "WorkerTestCube"

    # Create camera
    bpy.ops.object.camera_add(location=(5, -7, 5))
    camera = bpy.context.object

    direction = cube.location - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

    scene = bpy.context.scene
    scene.camera = camera

    # Create area light
    bpy.ops.object.light_add(type="AREA", location=(2, -4, 6))
    light = bpy.context.object
    light.data.energy = 500
    light.data.shape = "DISK"
    light.data.size = 5

    # Configure render
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 640
    scene.render.resolution_y = 640
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"

    scene.world.color = (0.12, 0.12, 0.12)


def main() -> None:
    output_path = get_output_path()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    build_test_scene()

    scene = bpy.context.scene
    scene.render.filepath = str(output_path)

    print("WORKER_SCENE_CREATED")
    print(f"RENDER_OUTPUT: {output_path}")

    bpy.ops.render.render(write_still=True)

    print("WORKER_RENDER_COMPLETED")


if __name__ == "__main__":
    main()
