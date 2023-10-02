import itertools
import math
import sys

from rayt_rust_py import (
    Lambertian,
    Ray,
    Vec3,
    random_double,
    unit_vector,
    write_color,
)

Color = Vec3
Point3 = Vec3


def ray_color(ray: Ray, world: Hittable, depth: int) -> Color:
    if depth <= 0:
        return Color(0.0, 0.0, 0.0)

    r_color = Color(1.0, 1.0, 1.0)

    for _ in range(depth, 0, -1):
        if (rec := world.hit(ray, 0.001, math.inf)) is not None:
            if None not in (scattered := rec.material.scatter(ray, rec)):
                ray, attenuation = scattered
                r_color *= attenuation
            else:
                return Color(0.0, 0.0, 0.0)
        else:
            unit_direction = unit_vector(ray.direction)
            t = 0.5 * (unit_direction.y + 1.0)
            r_color *= Color(1.0, 1.0, 1.0) * (1.0 - t) + Color(0.5, 0.7, 1.0) * t
            break

    return r_color


def random_scene() -> HittableList:
    world = HittableList()
    ground_material = Lambertian(albedo=Color(0.5, 0.5, 0.5))
    world.add(Sphere(Point3(0.0, -1000.0, 0.0), 1000.0, ground_material))

    for a, b in itertools.product(range(-11, 11), range(-11, 11)):
        choose_mat = random_double()
        center = Point3(a + 0.9 * random_double(), 0.2, b + 0.9 * random_double())

        if (center - Point3(4.0, 0.2, 0.0)).length > 0.9:
            if choose_mat < 0.8:
                # diffuse
                albedo = Color.random() * Color.random()
                sphere_material = Lambertian(albedo)
            elif choose_mat < 0.95:
                # metal
                albedo = Color.random(0.5, 1.0)
                fuzz = random_double(0.0, 0.5)
                sphere_material = Metal(albedo, fuzz)
            else:
                # glass
                sphere_material = Dielectric(1.5)

            world.add(Sphere(center, 0.2, sphere_material))

    material_1 = Dielectric(1.5)
    world.add(Sphere(Point3(0.0, 1.0, 0.0), 1.0, material_1))

    material_2 = Lambertian(Color(0.4, 0.2, 0.1))
    world.add(Sphere(Point3(-4.0, 1.0, 0.0), 1.0, material_2))

    material_3 = Metal(Color(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(Point3(4.0, 1.0, 0.0), 1.0, material_3))

    return world


def one_weekend(
    image_width: int = 300,
    samples_per_pixel: int = 20,
    max_depth: int = 50,
) -> None:
    aspect_ratio = 16.0 / 9.0
    image_height = int(image_width / aspect_ratio)
    world = random_scene()
    lookfrom = Point3(13, 2, 3)
    lookat = Point3(0, 0, 0)
    vup = Vec3(0, 1, 0)
    dist_to_focus = 10.0
    aperture = 0.1
    camera = Camera(lookfrom, lookat, vup, 20.0, aspect_ratio, aperture, dist_to_focus)

    print(f"P3\n{image_width} {image_height}\n255")

    for j, i in itertools.product(range(image_height - 1, -1, -1), range(image_width)):
        print(f"\rScanlines remaining: {j}", end=" ", file=sys.stderr)

        pixel_color = Color(0.0, 0.0, 0.0)

        for _ in range(1, samples_per_pixel + 1):
            u = (i + random_double()) / (image_width - 1)
            v = (j + random_double()) / (image_height - 1)
            ray = camera.get_ray(u, v)
            pixel_color += ray_color(ray, world, max_depth)

        write_color(pixel_color, samples_per_pixel)

    print("\nDone.", file=sys.stderr)
