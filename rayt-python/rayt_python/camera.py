import math

from rayt_python.ray import Ray
from rayt_python.utils import degrees_to_radians
from rayt_python.vec3 import (
    Point3,
    Vec3,
    cross,
    random_in_unit_disk,
    unit_vector,
)


class Camera:
    def __init__(
        self,
        lookfrom: Point3,
        lookat: Point3,
        vup: Vec3,
        vfov: float,
        aspect_ratio: float,
        aperture: float,
        focus_dist: float,
    ) -> None:
        theta = degrees_to_radians(vfov)
        h = math.tan(theta / 2)
        viewport_height = 2.0 * h
        viewport_width = aspect_ratio * viewport_height

        self.w = unit_vector(lookfrom - lookat)
        self.u = unit_vector(cross(vup, self.w))
        self.v = cross(self.w, self.u)

        self.origin = lookfrom
        self.horizontal = self.u * focus_dist * viewport_width
        self.vertical = self.v * focus_dist * viewport_height
        self.lower_left_corner = (
            self.origin - self.horizontal / 2 - self.vertical / 2 - self.w * focus_dist
        )
        self.lens_radius = aperture / 2

    def get_ray(self, s: float, t: float) -> Ray:
        rd = random_in_unit_disk() * self.lens_radius
        offset = self.u * rd.x + self.v * rd.y
        return Ray(
            self.origin + offset,
            self.lower_left_corner
            + self.horizontal * s
            + self.vertical * t
            - self.origin
            - offset,
        )
