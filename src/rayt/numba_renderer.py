import sys

import numpy as np
import numpy.typing as npt

from rayt_rust._core import Camera, HittableList, get_color, Color
from rayt.numba_optimized import render_pixel_numba


class NumbaRenderer:
    """Numba-optimized ray tracer renderer"""

    def __init__(self) -> None:
        self.spheres_data: npt.NDArray[np.float64] | None = None
        self.materials_data: npt.NDArray[np.float64] | None = None
        self.camera_data: npt.NDArray[np.float64] | None = None

    def _prepare_scene_data(self, world: HittableList, camera: Camera) -> None:
        """Convert scene objects to NumPy arrays for Numba"""
        # Sphere data: [center_x, center_y, center_z, radius]
        self.spheres_data = np.array(world.get_sphere_data(), dtype=np.float64)

        # Material data: [type, param1, param2, param3, param4]
        # Type 0: Lambertian [type, albedo_r, albedo_g, albedo_b, unused]
        # Type 1: Metal [type, albedo_r, albedo_g, albedo_b, fuzz]
        # Type 2: Dielectric [type, ref_idx, unused, unused, unused]
        # Default to Lambertian with white color
        self.materials_data = np.array(world.get_material_data(), dtype=np.float64)

        # Camera data: [origin, lower_left_corner, horizontal, vertical, lens_radius, u, v]
        self.camera_data = np.array(camera.get_data(), dtype=np.float64)

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
