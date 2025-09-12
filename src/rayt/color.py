import math

from rayt.vec3 import Color


def clamp(x: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(x, max_val))


def get_color(pixel_color: Color, samples_per_pixel: int) -> str:
    scale = 1.0 / samples_per_pixel

    def color_component(c: float) -> int:
        return int(255.999 * clamp(math.sqrt(scale * c), 0.0, 0.999))

    return f"{color_component(pixel_color.x)} {color_component(pixel_color.y)} {color_component(pixel_color.z)}"
