import math
from typing import Optional

from rayt.hittable import HitRecord, Hittable
from rayt.material import Material
from rayt.ray import Ray
from rayt.vec3 import Point3, Vec3, dot


class Sphere(Hittable):
    def __init__(self, center: Point3, radius: float, material: Material):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        oc = r.origin - self.center
        a = r.direction.length_squared
        half_b = dot(oc, r.direction)
        c = oc.length_squared - self.radius**2
        discriminant = half_b**2 - a * c

        if discriminant > 0:
            root = math.sqrt(discriminant)
            temp = (-half_b - root) / a
            if t_min < temp < t_max:
                t = temp
                p = r.at(t)
                outward_normal = (p - self.center) / self.radius
                rec = HitRecord(p, Vec3(), t, self.material)
                rec.set_face_normal(r, outward_normal)
                return rec

            temp = (-half_b + root) / a
            if t_min < temp < t_max:
                t = temp
                p = r.at(t)
                outward_normal = (p - self.center) / self.radius
                rec = HitRecord(p, Vec3(), t, self.material)
                rec.set_face_normal(r, outward_normal)
                return rec

        return None
