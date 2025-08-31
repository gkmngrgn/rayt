import math

from rayt.hittable import Hittable
from rayt.ray import Ray
from rayt.vec3 import Color, unit_vector

INFINITY = float("inf")


def clamp(x: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(x, max_val))


def get_color(pixel_color: Color, samples_per_pixel: int) -> str:
    scale = 1.0 / samples_per_pixel

    def color_component(c: float) -> int:
        return int(255.999 * clamp(math.sqrt(scale * c), 0.0, 0.999))

    return f"{color_component(pixel_color.x)} {color_component(pixel_color.y)} {color_component(pixel_color.z)}"


def ray_color(r: Ray, world: Hittable, depth: int) -> Color:
    if depth <= 0:
        return Color(0.0, 0.0, 0.0)

    if rec := world.hit(r, 0.001, INFINITY):
        if scattered_data := rec.material.scatter(r, rec):
            scattered, attenuation = scattered_data
            return attenuation * ray_color(scattered, world, depth - 1)
        return Color(0.0, 0.0, 0.0)

    # Sky gradient
    unit_direction = unit_vector(r.direction)
    t = 0.5 * (unit_direction.y + 1.0)
    return (1.0 - t) * Color(1.0, 1.0, 1.0) + t * Color(0.5, 0.7, 1.0)
