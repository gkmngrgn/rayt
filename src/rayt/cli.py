import itertools
import sys

import click

from rayt.camera import Camera
from rayt.hittable_list import HittableList
from rayt.numba_renderer import render_with_numba
from rayt.vec3 import Color, Point3, Vec3, random_double
from rayt.gpu_utils import get_render_engine, print_gpu_info, RenderEngine


def random_scene() -> HittableList:
    world = HittableList()
    world.add_lambertian(
        center=Point3(0.0, -1000.0, 0.0),
        radius=1000.0,
        albedo=Color(0.5, 0.5, 0.5),
    )

    for a, b in itertools.product(range(-11, 11), range(-11, 11)):
        choose_mat = random_double()
        center = Point3(a + 0.9 * random_double(), 0.2, b + 0.9 * random_double())
        radius = 0.2

        if (center - Point3(4.0, 0.2, 0.0)).length > 0.9:
            if choose_mat < 0.8:
                # diffuse
                world.add_lambertian(
                    center=center,
                    radius=radius,
                    albedo=Color.random() * Color.random(),
                )
            elif choose_mat < 0.95:
                # metal
                world.add_metal(
                    center=center,
                    radius=radius,
                    albedo=Color.random(min_max=(0.5, 1.0)),
                    fuzz=random_double(0.0, 0.5),
                )
            else:
                # glass
                world.add_dielectric(
                    center=center,
                    radius=radius,
                    ref_idx=1.5,
                )

    world.add_dielectric(
        center=Point3(0.0, 1.0, 0.0),
        radius=1.0,
        ref_idx=1.5,
    )
    world.add_lambertian(
        center=Point3(-4.0, 1.0, 0.0),
        radius=1.0,
        albedo=Color(0.4, 0.2, 0.1),
    )
    world.add_metal(
        center=Point3(4.0, 1.0, 0.0),
        radius=1.0,
        albedo=Color(0.7, 0.6, 0.5),
        fuzz=0.0,
    )

    return world


@click.command()
@click.option("--aspect-ratio", default=16.0 / 9.0, help="Image aspect ratio")
@click.option("--image-width", default=300, help="Image width in pixels")
@click.option("--samples-per-pixel", default=20, help="Number of samples per pixel")
@click.option("--max-depth", default=50, help="Maximum ray bounce depth")
@click.option("--engine", type=click.Choice(["auto", "cpu", "gpu"]), default="auto",
              help="Rendering engine: auto (detect best), cpu (force CPU), gpu (force GPU)")
@click.option("--prefer-gpu", is_flag=True, help="Prefer GPU when available (used with --engine=auto)")
@click.option("--gpu-info", is_flag=True, help="Show GPU information and exit")
def one_weekend(
    aspect_ratio: float,
    image_width: int,
    samples_per_pixel: int,
    max_depth: int,
    engine: str,
    prefer_gpu: bool,
    gpu_info: bool,
) -> None:
    # Show GPU info and exit if requested
    if gpu_info:
        print_gpu_info()
        return

    # Determine rendering engine
    force_engine: RenderEngine | None = None
    if engine == "cpu":
        force_engine = "cpu"
    elif engine == "gpu":
        force_engine = "gpu"

    selected_engine, reason = get_render_engine(
        prefer_gpu=prefer_gpu,
        force_engine=force_engine
    )

    print(f"Engine Selection: {reason}", file=sys.stderr)

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

    # Render with selected engine
    if selected_engine == "gpu":
        try:
            from rayt.cupy_renderer import render_with_cupy
            render_with_cupy(
                world, camera, image_width, image_height, samples_per_pixel, max_depth
            )
        except Exception as e:
            print(f"GPU rendering failed: {e}", file=sys.stderr)
            print("Falling back to CPU rendering", file=sys.stderr)
            render_with_numba(
                world, camera, image_width, image_height, samples_per_pixel, max_depth
            )
    else:
        render_with_numba(
            world, camera, image_width, image_height, samples_per_pixel, max_depth
        )
