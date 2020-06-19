from dataclasses import dataclass

from rayt_python.material import Material
from rayt_python.ray import Ray
from rayt_python.vec3 import Point3, Vec3, dot


@dataclass
class HitRecord:
    p: Point3
    normal: Vec3
    material: Material
    t: float
    front_face: bool

    def replace(self, rec: "HitRecord") -> None:
        self.p = rec.p
        self.normal = rec.normal
        self.material = rec.material
        self.t = rec.t
        self.front_face = rec.front_face

    def set_face_normal(self, ray: Ray, outward_normal: Vec3) -> None:
        self.front_face = dot(ray.direction(), outward_normal) < 0
        self.normal = outward_normal if self.front_face is True else -outward_normal


class Hittable:
    def hit(self, ray: Ray, t_min: float, t_max: float, rec: HitRecord) -> bool:
        raise NotImplementedError
