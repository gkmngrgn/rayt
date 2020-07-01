from rayt_python.utils import clamp
from rayt_python.vec3 import Color


def write_color(pixel_color: Color, samples_per_pixel: int) -> None:
    scale = 1.0 / samples_per_pixel
    get_color = lambda c: int(255.999 * clamp(pow(scale * c, 0.5), 0.0, 0.999))
    r = get_color(pixel_color.x)
    g = get_color(pixel_color.y)
    b = get_color(pixel_color.z)
    print(f"{r} {g} {b}")
