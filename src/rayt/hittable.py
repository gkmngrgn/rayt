from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

from rayt.ray import Ray
from rayt.vec3 import Point3, Vec3, dot

if TYPE_CHECKING:
    from rayt.material import Material


class HitRecord:
    def __init__(
        self,
        p: Point3,
        normal: Vec3,
        t: float,
        material: "Material",
        front_face: bool = False,
    ) -> None:
        self.p = p
        self.normal = normal
        self.t = t
        self.material = material
        self.front_face = front_face

    def set_face_normal(self, r: Ray, outward_normal: Vec3) -> None:
        self.front_face = dot(r.direction, outward_normal) < 0.0
        self.normal = outward_normal if self.front_face else -outward_normal


class Hittable(ABC):
    @abstractmethod
    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        pass
