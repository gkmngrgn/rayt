import sys

import numpy as np
import numpy.typing as npt

from rayt.camera import Camera
from rayt.color import get_color
from rayt.hittable_list import HittableList
from rayt.material import Dielectric, Lambertian, Metal
from rayt.sphere import Sphere
from rayt.vec3 import Color

try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False


# CuPy CUDA kernel for ray tracing
cupy_ray_tracer_kernel = r'''
#include <curand_kernel.h>

extern "C" __global__
void render_pixels(
    int image_width,
    int image_height,
    int samples_per_pixel,
    double* camera_data,
    double* spheres_data,
    double* materials_data,
    int n_spheres,
    int max_depth,
    double* output,
    unsigned long long seed
) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    int j = blockIdx.y * blockDim.y + threadIdx.y;

    if (i >= image_width || j >= image_height) return;

    int thread_id = j * image_width + i;

    // Initialize random state
    curandState state;
    curand_init(seed, thread_id, 0, &state);

    // Camera data
    double origin[3] = {camera_data[0], camera_data[1], camera_data[2]};
    double lower_left_corner[3] = {camera_data[3], camera_data[4], camera_data[5]};
    double horizontal[3] = {camera_data[6], camera_data[7], camera_data[8]};
    double vertical[3] = {camera_data[9], camera_data[10], camera_data[11]};

    double pixel_color[3] = {0.0, 0.0, 0.0};

    for (int s = 0; s < samples_per_pixel; s++) {
        double u = (i + curand_uniform_double(&state)) / (image_width - 1);
        double v = (j + curand_uniform_double(&state)) / (image_height - 1);

        // Ray direction
        double ray_direction[3] = {
            lower_left_corner[0] + u * horizontal[0] + v * vertical[0] - origin[0],
            lower_left_corner[1] + u * horizontal[1] + v * vertical[1] - origin[1],
            lower_left_corner[2] + u * horizontal[2] + v * vertical[2] - origin[2]
        };

        // Ray color computation (simplified for now)
        double current_origin[3] = {origin[0], origin[1], origin[2]};
        double current_direction[3] = {ray_direction[0], ray_direction[1], ray_direction[2]};
        double current_color[3] = {1.0, 1.0, 1.0};

        for (int depth = 0; depth < max_depth; depth++) {
            // Find closest hit
            double closest_t = 1e30;
            bool hit_found = false;
            int hit_sphere_idx = -1;
            double hit_point[3];
            double hit_normal[3];
            bool hit_front_face;

            for (int sphere_idx = 0; sphere_idx < n_spheres; sphere_idx++) {
                double sphere_center[3] = {
                    spheres_data[sphere_idx * 4 + 0],
                    spheres_data[sphere_idx * 4 + 1],
                    spheres_data[sphere_idx * 4 + 2]
                };
                double sphere_radius = spheres_data[sphere_idx * 4 + 3];

                // Ray-sphere intersection
                double oc[3] = {
                    current_origin[0] - sphere_center[0],
                    current_origin[1] - sphere_center[1],
                    current_origin[2] - sphere_center[2]
                };

                double a = current_direction[0] * current_direction[0] +
                          current_direction[1] * current_direction[1] +
                          current_direction[2] * current_direction[2];
                double half_b = oc[0] * current_direction[0] +
                               oc[1] * current_direction[1] +
                               oc[2] * current_direction[2];
                double c = oc[0] * oc[0] + oc[1] * oc[1] + oc[2] * oc[2] - sphere_radius * sphere_radius;
                double discriminant = half_b * half_b - a * c;

                if (discriminant > 0) {
                    double root = sqrt(discriminant);
                    double temp = (-half_b - root) / a;

                    if (temp > 0.001 && temp < closest_t) {
                        closest_t = temp;
                        hit_found = true;
                        hit_sphere_idx = sphere_idx;

                        hit_point[0] = current_origin[0] + temp * current_direction[0];
                        hit_point[1] = current_origin[1] + temp * current_direction[1];
                        hit_point[2] = current_origin[2] + temp * current_direction[2];

                        double outward_normal[3] = {
                            (hit_point[0] - sphere_center[0]) / sphere_radius,
                            (hit_point[1] - sphere_center[1]) / sphere_radius,
                            (hit_point[2] - sphere_center[2]) / sphere_radius
                        };

                        double dot_product = current_direction[0] * outward_normal[0] +
                                           current_direction[1] * outward_normal[1] +
                                           current_direction[2] * outward_normal[2];
                        hit_front_face = dot_product < 0.0;

                        if (hit_front_face) {
                            hit_normal[0] = outward_normal[0];
                            hit_normal[1] = outward_normal[1];
                            hit_normal[2] = outward_normal[2];
                        } else {
                            hit_normal[0] = -outward_normal[0];
                            hit_normal[1] = -outward_normal[1];
                            hit_normal[2] = -outward_normal[2];
                        }
                    }
                    else {
                        temp = (-half_b + root) / a;
                        if (temp > 0.001 && temp < closest_t) {
                            closest_t = temp;
                            hit_found = true;
                            hit_sphere_idx = sphere_idx;

                            hit_point[0] = current_origin[0] + temp * current_direction[0];
                            hit_point[1] = current_origin[1] + temp * current_direction[1];
                            hit_point[2] = current_origin[2] + temp * current_direction[2];

                            double outward_normal[3] = {
                                (hit_point[0] - sphere_center[0]) / sphere_radius,
                                (hit_point[1] - sphere_center[1]) / sphere_radius,
                                (hit_point[2] - sphere_center[2]) / sphere_radius
                            };

                            double dot_product = current_direction[0] * outward_normal[0] +
                                               current_direction[1] * outward_normal[1] +
                                               current_direction[2] * outward_normal[2];
                            hit_front_face = dot_product < 0.0;

                            if (hit_front_face) {
                                hit_normal[0] = outward_normal[0];
                                hit_normal[1] = outward_normal[1];
                                hit_normal[2] = outward_normal[2];
                            } else {
                                hit_normal[0] = -outward_normal[0];
                                hit_normal[1] = -outward_normal[1];
                                hit_normal[2] = -outward_normal[2];
                            }
                        }
                    }
                }
            }

            if (!hit_found) {
                // Sky gradient
                double unit_dir_len = sqrt(current_direction[0] * current_direction[0] +
                                         current_direction[1] * current_direction[1] +
                                         current_direction[2] * current_direction[2]);
                double unit_direction_y = current_direction[1] / unit_dir_len;
                double t = 0.5 * (unit_direction_y + 1.0);

                double sky_r = (1.0 - t) * 1.0 + t * 0.5;
                double sky_g = (1.0 - t) * 1.0 + t * 0.7;
                double sky_b = (1.0 - t) * 1.0 + t * 1.0;

                pixel_color[0] += current_color[0] * sky_r;
                pixel_color[1] += current_color[1] * sky_g;
                pixel_color[2] += current_color[2] * sky_b;
                break;
            }

            // Material scattering (simplified - Lambertian only for now)
            int material_type = (int)materials_data[hit_sphere_idx * 5 + 0];

            if (material_type == 0) { // Lambertian
                double albedo_r = materials_data[hit_sphere_idx * 5 + 1];
                double albedo_g = materials_data[hit_sphere_idx * 5 + 2];
                double albedo_b = materials_data[hit_sphere_idx * 5 + 3];

                current_color[0] *= albedo_r;
                current_color[1] *= albedo_g;
                current_color[2] *= albedo_b;

                // Random direction in unit sphere
                double random_dir[3];
                do {
                    random_dir[0] = curand_uniform_double(&state) * 2.0 - 1.0;
                    random_dir[1] = curand_uniform_double(&state) * 2.0 - 1.0;
                    random_dir[2] = curand_uniform_double(&state) * 2.0 - 1.0;
                } while (random_dir[0]*random_dir[0] + random_dir[1]*random_dir[1] + random_dir[2]*random_dir[2] >= 1.0);

                current_origin[0] = hit_point[0];
                current_origin[1] = hit_point[1];
                current_origin[2] = hit_point[2];

                current_direction[0] = hit_normal[0] + random_dir[0];
                current_direction[1] = hit_normal[1] + random_dir[1];
                current_direction[2] = hit_normal[2] + random_dir[2];
            } else {
                // For simplicity, treat other materials as absorbing
                pixel_color[0] += 0.0;
                pixel_color[1] += 0.0;
                pixel_color[2] += 0.0;
                break;
            }
        }
    }

    // Store result (note: j is flipped for correct image orientation)
    int output_idx = ((image_height - 1 - j) * image_width + i) * 3;
    output[output_idx + 0] = pixel_color[0];
    output[output_idx + 1] = pixel_color[1];
    output[output_idx + 2] = pixel_color[2];
}
'''


class CupyRenderer:
    """CuPy-accelerated ray tracer renderer"""

    def __init__(self) -> None:
        self.spheres_data: npt.NDArray[np.float64] | None = None
        self.materials_data: npt.NDArray[np.float64] | None = None
        self.camera_data: npt.NDArray[np.float64] | None = None
        self.kernel = None

    def _prepare_scene_data(self, world: HittableList, camera: Camera) -> None:
        """Convert scene objects to NumPy arrays for CuPy"""
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
        """Render using CuPy acceleration"""
        if not CUPY_AVAILABLE:
            raise RuntimeError("CuPy not available. Please install CuPy: uv add --optional cuda")

        print(
            f"Rendering {image_width}x{image_height} with CuPy GPU acceleration",
            file=sys.stderr,
        )
        print(
            f"Samples per pixel: {samples_per_pixel}, Max depth: {max_depth}",
            file=sys.stderr,
        )

        # Prepare scene data
        self._prepare_scene_data(world, camera)

        # Calculate optimal block and grid sizes
        block_size = (16, 16)
        grid_size = (
            (image_width + block_size[0] - 1) // block_size[0],
            (image_height + block_size[1] - 1) // block_size[1]
        )

        print(f"CUDA grid size: {grid_size}, block size: {block_size}", file=sys.stderr)

        # Transfer data to GPU
        d_spheres_data = cp.asarray(self.spheres_data.flatten())
        d_materials_data = cp.asarray(self.materials_data.flatten())
        d_camera_data = cp.asarray(self.camera_data)

        # Allocate output array on GPU
        output_shape = (image_height * image_width * 3,)
        d_output = cp.zeros(output_shape, dtype=np.float64)

        # Compile and launch kernel
        print("Compiling CUDA kernel...", file=sys.stderr)
        self.kernel = cp.RawKernel(cupy_ray_tracer_kernel, 'render_pixels')

        print("Launching CUDA kernel...", file=sys.stderr)

        # Launch CUDA kernel
        self.kernel(
            grid_size,
            block_size,
            args=(
                image_width,
                image_height,
                samples_per_pixel,
                d_camera_data,
                d_spheres_data,
                d_materials_data,
                len(world.objects),
                max_depth,
                d_output,
                np.uint64(42)  # seed
            )
        )

        # Wait for GPU to complete
        cp.cuda.Stream.null.synchronize()
        print("CUDA kernel completed", file=sys.stderr)

        # Transfer result back to host
        output = d_output.get().reshape(image_height, image_width, 3)

        # Output PPM header
        print("P3")
        print(f"{image_width} {image_height}")
        print("255")

        # Output image data
        for j in range(image_height):
            print(f"\rConverting scanlines: {j+1}/{image_height}", end=" ", file=sys.stderr)

            for i in range(image_width):
                # Convert back to Color object for output
                pixel_color = Color(
                    output[j, i, 0], output[j, i, 1], output[j, i, 2]
                )
                print(get_color(pixel_color, samples_per_pixel))

        print("\nDone.", file=sys.stderr)


def render_with_cupy(
    world: HittableList,
    camera: Camera,
    image_width: int,
    image_height: int,
    samples_per_pixel: int,
    max_depth: int,
) -> None:
    """Main function for CuPy-accelerated rendering"""
    renderer = CupyRenderer()
    renderer.render(
        world, camera, image_width, image_height, samples_per_pixel, max_depth
    )
