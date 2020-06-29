import typing

from rayt_python.hittable import HitRecord, Hittable
from rayt_python.material import Material
from rayt_python.ray import Ray
from rayt_python.vec3 import Point3, dot


class Sphere(Hittable):
    def __init__(self, cen: Point3, r: float, m: Material) -> None:
        self.center = cen
        self.radius = r
        self.material = m

    def create_rec(self, ray: Ray, t: float) -> HitRecord:
        p = ray.at(t)
        rec = HitRecord(p=p, t=t, material=self.material)
        rec.set_face_normal(ray, (p - self.center) / self.radius)
        return rec

    def hit(self, r: Ray, t_min: float, t_max: float) -> typing.Union[HitRecord, None]:
        oc = r.origin - self.center
        a = r.direction.length_squared
        half_b = dot(oc, r.direction)
        c = oc.length_squared - pow(self.radius, 2)
        discriminant = pow(half_b, 2) - a * c

        if discriminant > 0:
            root = pow(discriminant, 0.5)
            temp = (-half_b - root) / a
            if temp < t_max and temp > t_min:
                return self.create_rec(r, temp)

            temp = (-half_b + root) / a
            if t_min < temp < t_max:
                return self.create_rec(r, temp)

        return None
