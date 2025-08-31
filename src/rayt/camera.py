import math

from rayt.ray import Ray
from rayt.vec3 import Point3, Vec3, cross, random_in_unit_disk, unit_vector


def degrees_to_radians(degrees: float) -> float:
    return degrees * math.pi / 180.0


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
    ):
        theta = degrees_to_radians(vfov)
        h = math.tan(theta / 2.0)
        viewport_height = 2.0 * h
        viewport_width = aspect_ratio * viewport_height

        w = unit_vector(lookfrom - lookat)
        u = unit_vector(cross(vup, w))
        v = cross(w, u)

        self.origin = lookfrom
        self.horizontal = focus_dist * viewport_width * u
        self.vertical = focus_dist * viewport_height * v
        self.lower_left_corner = (
            self.origin - self.horizontal / 2.0 - self.vertical / 2.0 - focus_dist * w
        )
        self.lens_radius = aperture / 2.0
        self.u = u
        self.v = v

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
