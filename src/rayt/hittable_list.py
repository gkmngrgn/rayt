from typing import List, Optional

from rayt.hittable import HitRecord, Hittable
from rayt.material import Dielectric, Lambertian, Metal
from rayt.ray import Ray
from rayt.sphere import Sphere
from rayt.vec3 import Color, Point3


class HittableList(Hittable):
    def __init__(self) -> None:
        self.objects: List[Hittable] = []

    def clear(self) -> None:
        self.objects.clear()

    def add(self, obj: Hittable) -> None:
        self.objects.append(obj)

    def add_lambertian(self, center: Point3, radius: float, albedo: Color) -> None:
        material = Lambertian(albedo)
        sphere = Sphere(center, radius, material)
        self.add(sphere)

    def add_metal(
        self, center: Point3, radius: float, albedo: Color, fuzz: float
    ) -> None:
        material = Metal(albedo, fuzz)
        sphere = Sphere(center, radius, material)
        self.add(sphere)

    def add_dielectric(self, center: Point3, radius: float, ref_idx: float) -> None:
        material = Dielectric(ref_idx)
        sphere = Sphere(center, radius, material)
        self.add(sphere)

    def hit(self, r: Ray, t_min: float, t_max: float) -> Optional[HitRecord]:
        temp_rec = None
        hit_anything = False
        closest_so_far = t_max

        for obj in self.objects:
            if rec := obj.hit(r, t_min, closest_so_far):
                hit_anything = True
                closest_so_far = rec.t
                temp_rec = rec

        return temp_rec if hit_anything else None
