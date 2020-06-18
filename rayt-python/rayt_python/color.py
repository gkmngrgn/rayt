import math

from rayt_python.utils import clamp
from rayt_python.vec3 import Color


def write_color(pixel_color: Color, samples_per_pixel: int) -> None:
    scale = 1.0 / samples_per_pixel

    def color_(c: float) -> int:
        return int(255.999 * clamp(math.sqrt(scale * c), 0.0, 0.999))

    r = color_(pixel_color.x())
    g = color_(pixel_color.y())
    b = color_(pixel_color.z())

    print(f"{r} {g} {b}")
