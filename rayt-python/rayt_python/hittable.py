import typing
from dataclasses import dataclass

from rayt_python.material import Material
from rayt_python.ray import Ray
from rayt_python.vec3 import Point3, Vec3, dot


@dataclass
class HitRecord:
    p: Point3 = Point3(0.0, 0.0, 0.0)
    normal: Vec3 = Vec3(0.0, 0.0, 0.0)
    material: Material = Material()
    t: float = 0.0
    front_face: bool = False

    def update(self, rec: "HitRecord") -> None:
        self.p = rec.p
        self.normal = rec.normal
        self.material = rec.material
        self.t = rec.t
        self.front_face = rec.front_face

    def set_face_normal(self, ray: Ray, outward_normal: Vec3) -> None:
        self.front_face = dot(ray.direction, outward_normal) < 0
        self.normal = outward_normal if self.front_face is True else -outward_normal


class Hittable:
    def hit(
        self, ray: Ray, t_min: float, t_max: float, rec: HitRecord
    ) -> typing.NoReturn:
        raise NotImplementedError
