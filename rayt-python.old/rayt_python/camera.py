import math

from rayt_python.ray import Ray
from rayt_python.utils import degrees_to_radians
from rayt_python.vec3 import cross, random_in_unit_disk, unit_vector
from rayt_python.vec3_types import Point3, Vec3


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
        self.horizontal = focus_dist * viewport_width * self.u
        self.vertical = focus_dist * viewport_height * self.v
        self.lower_left_corner = (
            self.origin
            - self.horizontal / 2.0
            - self.vertical / 2.0
            - focus_dist * self.w
        )
        self.lens_radius = aperture / 2

    def get_ray(self, s: float, t: float) -> Ray:
        rd = self.lens_radius * random_in_unit_disk()
        offset = self.u * rd.x + self.v * rd.y
        return Ray(
            self.origin + offset,
            self.lower_left_corner
            + s * self.horizontal
            + t * self.vertical
            - self.origin
            - offset,
        )
