import math
import sys

from rayt_python.camera import Camera
from rayt_python.color import write_color
from rayt_python.hittable import HitRecord, Hittable
from rayt_python.hittable_list import HittableList
from rayt_python.material import Dielectric, Lambertian, Metal
from rayt_python.ray import Ray
from rayt_python.sphere import Sphere
from rayt_python.utils import random_double
from rayt_python.vec3 import Color, Point3, Vec3, dot, unit_vector


def hit_sphere(center: Point3, radius: float, ray: Ray) -> float:
    oc = ray.origin - center
    a = ray.direction.length_squared
    half_b = dot(oc, ray.direction)
    c = oc.length_squared - radius * radius
    discriminant = pow(half_b, 2) - a * c
    return -1.0 if discriminant < 0 else (-half_b - pow(discriminant, 0.5)) / a


def ray_color(ray: Ray, world: Hittable, depth: int) -> Color:
    if depth <= 0:
        return Color(0.0, 0.0, 0.0)

    rec = HitRecord()

    if world.hit(ray, 0.001, math.inf, rec):
        scattered = Ray(origin=Color(1.0, 1.0, 1.0), direction=Vec3(1.0, 1.0, 1.0))
        scattered = Ray(origin=Color(0.0, 0.0, 0.0), direction=Vec3(0.0, 0.0, 0.0))
        attenuation = Color(0.0, 0.0, 0.0)
        if rec.material.scatter(ray, rec, attenuation, scattered):
            return attenuation * ray_color(scattered, world, depth - 1)
        return Color(0.0, 0.0, 0.0)

    unit_direction = unit_vector(ray.direction)
    t = 0.5 * (unit_direction.y + 1.0)
    return Color(1.0, 1.0, 1.0) * (1.0 - t) + Color(0.5, 0.7, 1.0) * t


def random_scene() -> HittableList:
    world = HittableList()
    ground_material = Lambertian(albedo=Color(0.5, 0.5, 0.5))
    world.add(Sphere(Point3(0, -1000, 0), 1000, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random_double()
            center = Point3(a + 0.9 * random_double(), 0.2, b + 0.9 * random_double())

            if (center - Point3(4, 0.2, 0)).length > 0.9:
                if choose_mat < 0.8:
                    # diffuse
                    albedo = Color.random() * Color.random()
                    sphere_material = Lambertian(albedo)
                    world.add(Sphere(center, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    # metal
                    albedo = Color.random(0.5, 1)
                    fuzz = random_double(0, 0.5)
                    sphere_material = Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                else:
                    # glass
                    sphere_material = Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))

    material_1 = Dielectric(1.5)
    world.add(Sphere(Point3(0, 1, 0), 1.0, material_1))

    material_2 = Lambertian(Color(0.4, 0.2, 0.1))
    world.add(Sphere(Point3(-4, 1, 0), 1.0, material_2))

    material_3 = Metal(Color(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(Point3(4, 1, 0), 1.0, material_3))

    return world


def main() -> None:
    aspect_ratio = 16.0 / 9.0
    image_width = 1200
    image_height = int(image_width / aspect_ratio)
    samples_per_pixel = 20
    max_depth = 50

    print(f"P3\n{image_width} {image_height}\n255")

    world = random_scene()

    lookfrom = Point3(13, 2, 3)
    lookat = Point3(0, 0, 0)
    vup = Vec3(0, 1, 0)
    dist_to_focus = 10.0
    aperture = 0.1

    cam = Camera(lookfrom, lookat, vup, 20, aspect_ratio, aperture, dist_to_focus)

    for j in range(image_height - 1, -1, -1):
        print(f"\rScanlines remaining: {j}", file=sys.stderr, end="", flush=True)

        for i in range(1, image_width + 1):
            pixel_color = Color(0.0, 0.0, 0.0)

            for s in range(1, samples_per_pixel + 1):
                u = (i + random_double()) / (image_width - 1)
                v = (j + random_double()) / (image_height - 1)
                ray = cam.get_ray(u, v)
                pixel_color += ray_color(ray, world, max_depth)

            write_color(pixel_color, samples_per_pixel)

    print("\nDone.", file=sys.stderr)
