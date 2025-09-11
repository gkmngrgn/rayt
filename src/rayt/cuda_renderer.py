import sys

import numpy as np
import numpy.typing as npt

from rayt.camera import Camera
from rayt.color import get_color
from rayt.hittable_list import HittableList
from rayt.material import Dielectric, Lambertian, Metal
from rayt.sphere import Sphere
from rayt.vec3 import Color

from numba import cuda
from numba.cuda.random import create_xoroshiro128p_states
from rayt.cuda_optimized import render_pixels_cuda


class CudaRenderer:
    """CUDA-accelerated ray tracer renderer"""

    def __init__(self) -> None:
        self.spheres_data: npt.NDArray[np.float64] | None = None
        self.materials_data: npt.NDArray[np.float64] | None = None
        self.camera_data: npt.NDArray[np.float64] | None = None

    def _prepare_scene_data(self, world: HittableList, camera: Camera) -> None:
        """Convert scene objects to NumPy arrays for CUDA"""
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
        """Render using CUDA acceleration"""
        print(
            f"Rendering {image_width}x{image_height} with CUDA GPU acceleration",
            file=sys.stderr,
        )
        print(
            f"Samples per pixel: {samples_per_pixel}, Max depth: {max_depth}",
            file=sys.stderr,
        )

        # Prepare scene data for CUDA
        self._prepare_scene_data(world, camera)

        # Explicitly select CUDA device 0 to avoid IndexError
        cuda.select_device(0)

        # Calculate optimal block and grid sizes
        block_size = (16, 16)
        grid_size = (
            (image_width + block_size[0] - 1) // block_size[0],
            (image_height + block_size[1] - 1) // block_size[1],
        )

        print(f"CUDA grid size: {grid_size}, block size: {block_size}", file=sys.stderr)

        # Transfer data to GPU
        d_spheres_data = cuda.to_device(self.spheres_data)
        d_materials_data = cuda.to_device(self.materials_data)
        d_camera_data = cuda.to_device(self.camera_data)

        # Allocate output array on GPU
        output_shape = (image_height, image_width, 3)
        d_output = cuda.device_array(output_shape, dtype=np.float64)

        # Initialize random number generator states
        total_threads = image_width * image_height
        rng_states = create_xoroshiro128p_states(total_threads, seed=42)

        print("Launching CUDA kernel...", file=sys.stderr)

        # Launch CUDA kernel
        render_pixels_cuda[grid_size, block_size](
            image_width,
            image_height,
            samples_per_pixel,
            d_camera_data,
            d_spheres_data,
            d_materials_data,
            max_depth,
            rng_states,
            d_output,
        )

        # Wait for GPU to complete
        cuda.synchronize()
        print("CUDA kernel completed", file=sys.stderr)

        # Transfer result back to host
        output = d_output.copy_to_host()

        # Output PPM header
        print("P3")
        print(f"{image_width} {image_height}")
        print("255")

        # Output image data
        for j in range(image_height):
            print(
                f"\rConverting scanlines: {j + 1}/{image_height}",
                end=" ",
                file=sys.stderr,
            )

            for i in range(image_width):
                # Convert back to Color object for output
                pixel_color = Color(output[j, i, 0], output[j, i, 1], output[j, i, 2])
                print(get_color(pixel_color, samples_per_pixel))

        print("\nDone.", file=sys.stderr)


def render_with_cuda(
    world: HittableList,
    camera: Camera,
    image_width: int,
    image_height: int,
    samples_per_pixel: int,
    max_depth: int,
) -> None:
    """Main function for CUDA-accelerated rendering"""
    renderer = CudaRenderer()
    renderer.render(
        world, camera, image_width, image_height, samples_per_pixel, max_depth
    )
