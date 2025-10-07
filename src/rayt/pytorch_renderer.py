import sys
import torch

from rayt_rust._core import Camera, HittableList, get_color, Color
from rayt.pytorch_optimized import render_pixel_torch


class PyTorchRenderer:
    """PyTorch-optimized ray tracer renderer"""

    def __init__(self, device="cpu"):
        self.device = device
        self.spheres_data = None
        self.materials_data = None
        self.camera_data = None

    def _prepare_scene_data(self, world: HittableList, camera: Camera) -> None:
        """Convert scene objects to PyTorch tensors"""
        # Sphere data
        self.spheres_data = torch.tensor(world.get_sphere_data(), dtype=torch.float64, device=self.device)

        # Material data
        self.materials_data = torch.tensor(world.get_material_data(), dtype=torch.float64, device=self.device)

        # Camera data
        self.camera_data = torch.tensor(camera.get_data(), dtype=torch.float64, device=self.device)

    def render(
        self,
        world: HittableList,
        camera: Camera,
        image_width: int,
        image_height: int,
        samples_per_pixel: int,
        max_depth: int,
    ) -> None:
        """Render using PyTorch optimization"""
        print(
            f"Rendering {image_width}x{image_height} with PyTorch on {self.device}",
            file=sys.stderr,
        )
        print(
            f"Samples per pixel: {samples_per_pixel}, Max depth: {max_depth}",
            file=sys.stderr,
        )

        self._prepare_scene_data(world, camera)

        # Output PPM header
        print("P3")
        print(f"{image_width} {image_height}")
        print("255")

        # Render image
        for j in range(image_height, 0, -1):
            print(f"\rScanlines remaining: {j}", end=" ", file=sys.stderr)

            for i in range(image_width):
                pixel_color_tensor = render_pixel_torch(
                    i,
                    j - 1,
                    image_width,
                    image_height,
                    samples_per_pixel,
                    self.camera_data,
                    self.spheres_data,
                    self.materials_data,
                    max_depth,
                    self.device,
                )

                # Convert tensor to Color object for output
                pixel_color_cpu = pixel_color_tensor.cpu()
                pixel_color = Color(
                    pixel_color_cpu[0].item(), pixel_color_cpu[1].item(), pixel_color_cpu[2].item()
                )
                print(get_color(pixel_color, samples_per_pixel))

        print("\nDone.", file=sys.stderr)


def render_with_pytorch(
    world: HittableList,
    camera: Camera,
    image_width: int,
    image_height: int,
    samples_per_pixel: int,
    max_depth: int,
    use_gpu: bool = False,
) -> None:
    """Main function for PyTorch-accelerated rendering"""
    device = "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
    if use_gpu and not torch.cuda.is_available():
        print("GPU not available, falling back to CPU", file=sys.stderr)

    renderer = PyTorchRenderer(device=device)
    renderer.render(
        world, camera, image_width, image_height, samples_per_pixel, max_depth
    )