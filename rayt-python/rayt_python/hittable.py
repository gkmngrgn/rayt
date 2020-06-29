import typing

from rayt_python.material import Material
from rayt_python.ray import Ray
from rayt_python.vec3 import Point3, Vec3, dot


class HitRecord:
    def __init__(self, p: Point3, t: float, material: Material) -> None:
        self.p = p
        self.t = t
        self.material = material
        self.front_face = False
        self.normal = Vec3(0.0, 0.0, 0.0)

    def set_face_normal(self, ray: Ray, outward_normal: Vec3) -> None:
        self.front_face = dot(ray.direction, outward_normal) < 0
        self.normal = outward_normal if self.front_face is True else -outward_normal


class Hittable:
    def hit(self, ray: Ray, t_min: float, t_max: float) -> typing.NoReturn:
        raise NotImplementedError
