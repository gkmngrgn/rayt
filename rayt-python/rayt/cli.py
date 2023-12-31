import itertools
import sys

import click
from rayt_python import Camera, HittableList, Vec3, get_color, random_double, ray_color

Color = Vec3
Point3 = Vec3


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
@click.option("--aspect-ratio", default=16.0 / 9.0)
@click.option("--image-width", default=300)
@click.option("--samples-per-pixel", default=20)
@click.option("--max-depth", default=50)
def one_weekend(
    aspect_ratio: float,
    image_width: int,
    samples_per_pixel: int,
    max_depth: int,
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

    print("P3")
    print(f"{image_width} {image_height}")
    print("255")

    for j in range(image_height, 0, -1):
        print(f"\rScanlines remaining: {j}", end=" ", file=sys.stderr)

        for i in range(image_width):
            pixel_color = Color(0.0, 0.0, 0.0)

            for _ in range(1, samples_per_pixel + 1):
                u = (i + random_double()) / (image_width - 1)
                v = (j + random_double()) / (image_height - 1)
                ray = camera.get_ray(u, v)
                pixel_color += ray_color(ray, world, max_depth)

            print(get_color(pixel_color, samples_per_pixel))

    print("\nDone.", file=sys.stderr)
