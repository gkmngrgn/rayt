import math

from rayt_python.hittable import HitRecord, Hittable
from rayt_python.material import Material
from rayt_python.ray import Ray
from rayt_python.vec3 import Point3, dot


class Sphere(Hittable):
    def __init__(self, cen: Point3 = None, r: float = None, m: Material = None) -> None:
        self.center = cen
        self.radius = r
        self.material = m

    def hit(self, r: Ray, t_min: float, t_max: float, rec: HitRecord) -> bool:
        oc = r.origin() - self.center
        a = r.direction().length_squared()
        half_b = dot(oc, r.direction())
        c = oc.length_squared() - self.radius * self.radius
        discriminant = half_b * half_b - a * c

        if discriminant > 0:
            root = math.sqrt(discriminant)
            temp = (-half_b - root) / a
            if temp < t_max and temp > t_min:
                rec.t = temp
                rec.p = r.at(rec.t)
                rec.normal = (rec.p - self.center) / self.radius
                outward_normal = (rec.p - self.center) / self.radius  # TODO: why?
                rec.set_face_normal(r, outward_normal)
                rec.material = self.material
                return True

            temp = (-half_b + root) / a
            if t_min < temp < t_max:
                rec.t = temp
                rec.p = r.at(rec.t)
                rec.normal = (
                    rec.p - self.center
                ) / self.radius  # TODO: I'm repeating again and again
                outward_normal = (rec.p - self.center) / self.radius
                rec.set_face_normal(r, outward_normal)
                rec.material = self.material
                return True

        return False
