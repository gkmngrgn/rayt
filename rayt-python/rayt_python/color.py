from rayt_python.utils import clamp
from rayt_python.vec3_types import Color


def get_color_str(pixel_color: Color, samples_per_pixel: int) -> str:
    scale = 1.0 / samples_per_pixel
    get_color = lambda c: int(255.999 * clamp(pow(scale * c, 0.5), 0.0, 0.999))
    r = get_color(pixel_color.x)
    g = get_color(pixel_color.y)
    b = get_color(pixel_color.z)
    return f"{r} {g} {b}"


def write_color(pixel_color: Color, samples_per_pixel: int) -> None:
    print(get_color_str(pixel_color, samples_per_pixel))
