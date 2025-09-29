import click

from rayt.scene import random_scene
from rayt_rust._core import Camera, Vec3, Point3


@click.command()
@click.option("--aspect-ratio", default=16.0 / 9.0, help="Image aspect ratio")
@click.option("--image-width", default=300, help="Image width in pixels")
@click.option("--samples-per-pixel", default=20, help="Number of samples per pixel")
@click.option("--max-depth", default=50, help="Maximum ray bounce depth")
@click.option(
    "--engine",
    type=click.Choice(["numba", "cuda", "rust"]),
    default="numba",
    help="Rendering engine: cpu (force CPU), gpu (force GPU)",
)
def one_weekend(
    aspect_ratio: float,
    image_width: int,
    samples_per_pixel: int,
    max_depth: int,
    engine: str,
) -> None:
    image_height = int(image_width / aspect_ratio)
    world = random_scene()
    camera = Camera(
        lookfrom=Point3(13, 2, 3),
        lookat=Point3(0, 0, 0),
        vup=Vec3(0, 1, 0),
        vfov=20.0,
        aspect_ratio=aspect_ratio,
        aperture=0.1,
        focus_dist=10.0,
    )

    match engine:
        case "cuda":
            from rayt.cuda_renderer import render_with_cuda

            render_func = render_with_cuda
        case "numba":
            from rayt.numba_renderer import render_with_numba

            render_func = render_with_numba
        case _:
            from rayt.rust_renderer import render_with_rust

            render_func = render_with_rust

    render_func(world, camera, image_width, image_height, samples_per_pixel, max_depth)


@click.command()
def test_gpu_availability() -> None:
    from rayt.gpu_utils import detect_gpu_capabilities

    detect_gpu_capabilities()
