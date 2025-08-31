import sys

import numpy as np
import numpy.typing as npt

from rayt.camera import Camera
from rayt.color import get_color
from rayt.hittable_list import HittableList
from rayt.material import Dielectric, Lambertian, Metal
from rayt.numba_optimized import render_pixel_numba
from rayt.sphere import Sphere
from rayt.vec3 import Color


class NumbaRenderer:
    """Numba-optimized ray tracer renderer"""

    def __init__(self) -> None:
        self.spheres_data: npt.NDArray[np.float64] | None = None
        self.materials_data: npt.NDArray[np.float64] | None = None
        self.camera_data: npt.NDArray[np.float64] | None = None

    def _prepare_scene_data(self, world: HittableList, camera: Camera) -> None:
        """Convert scene objects to NumPy arrays for Numba"""
        spheres = []
        materials = []

        for obj in world.objects:
            if isinstance(obj, Sphere):
                # Sphere data: [center_x, center_y, center_z, radius]
                sphere_data = [obj.center.x, obj.center.y, obj.center.z, obj.radius]
                spheres.append(sphere_data)

                # Material data: [type, param1, param2, param3, param4]
                if isinstance(obj.material, Lambertian):
                    # Type 0: Lambertian [type, albedo_r, albedo_g, albedo_b, unused]
                    material_data = [
                        0,
                        obj.material.albedo.x,
                        obj.material.albedo.y,
                        obj.material.albedo.z,
                        0.0,
                    ]
                elif isinstance(obj.material, Metal):
                    # Type 1: Metal [type, albedo_r, albedo_g, albedo_b, fuzz]
                    material_data = [
                        1,
                        obj.material.albedo.x,
                        obj.material.albedo.y,
                        obj.material.albedo.z,
                        obj.material.fuzz,
                    ]
                elif isinstance(obj.material, Dielectric):
                    # Type 2: Dielectric [type, ref_idx, unused, unused, unused]
                    material_data = [2, obj.material.ref_idx, 0.0, 0.0, 0.0]
                else:
                    # Default to Lambertian with white color
                    material_data = [0, 1.0, 1.0, 1.0, 0.0]

                materials.append(material_data)

        self.spheres_data = np.array(spheres, dtype=np.float64)
        self.materials_data = np.array(materials, dtype=np.float64)

        # Camera data: [origin, lower_left_corner, horizontal, vertical, lens_radius, u, v]
        self.camera_data = np.array(
            [
                camera.origin.x,
                camera.origin.y,
                camera.origin.z,
                camera.lower_left_corner.x,
                camera.lower_left_corner.y,
                camera.lower_left_corner.z,
                camera.horizontal.x,
                camera.horizontal.y,
                camera.horizontal.z,
                camera.vertical.x,
                camera.vertical.y,
                camera.vertical.z,
                camera.lens_radius,
                camera.u.x,
                camera.u.y,
                camera.u.z,
                camera.v.x,
                camera.v.y,
                camera.v.z,
            ],
            dtype=np.float64,
        )

    def render(
        self,
        world: HittableList,
        camera: Camera,
        image_width: int,
        image_height: int,
        samples_per_pixel: int,
        max_depth: int,
    ) -> None:
        """Render using Numba optimization"""
        print(
            f"Rendering {image_width}x{image_height} with Numba JIT optimization",
            file=sys.stderr,
        )
        print(
            f"Samples per pixel: {samples_per_pixel}, Max depth: {max_depth}",
            file=sys.stderr,
        )

        # Prepare scene data for Numba
        self._prepare_scene_data(world, camera)

        # Trigger JIT compilation with a small test
        print("JIT compiling (first run may be slow)...", file=sys.stderr)
        render_pixel_numba(
            0,
            0,
            image_width,
            image_height,
            1,
            self.camera_data,
            self.spheres_data,
            self.materials_data,
            max_depth,
        )
        print("JIT compilation completed", file=sys.stderr)

        # Output PPM header
        print("P3")
        print(f"{image_width} {image_height}")
        print("255")

        # Render image
        for j in range(image_height, 0, -1):
            print(f"\rScanlines remaining: {j}", end=" ", file=sys.stderr)

            for i in range(image_width):
                pixel_color_array = render_pixel_numba(
                    i,
                    j - 1,
                    image_width,
                    image_height,
                    samples_per_pixel,
                    self.camera_data,
                    self.spheres_data,
                    self.materials_data,
                    max_depth,
                )

                # Convert back to Color object for output
                pixel_color = Color(
                    pixel_color_array[0], pixel_color_array[1], pixel_color_array[2]
                )
                print(get_color(pixel_color, samples_per_pixel))

        print("\nDone.", file=sys.stderr)


def render_with_numba(
    world: HittableList,
    camera: Camera,
    image_width: int,
    image_height: int,
    samples_per_pixel: int,
    max_depth: int,
) -> None:
    """Main function for Numba-accelerated rendering"""
    renderer = NumbaRenderer()
    renderer.render(
        world, camera, image_width, image_height, samples_per_pixel, max_depth
    )
