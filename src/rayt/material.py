from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Tuple

from rayt.ray import Ray
from rayt.vec3 import (
    Color,
    dot,
    random_double,
    random_in_unit_sphere,
    random_unit_vector,
    reflect,
    refract,
    unit_vector,
)

if TYPE_CHECKING:
    from rayt.hittable import HitRecord


class Material(ABC):
    @abstractmethod
    def scatter(self, r_in: Ray, rec: "HitRecord") -> Optional[Tuple[Ray, Color]]:
        pass


class Lambertian(Material):
    def __init__(self, albedo: Color):
        self.albedo = albedo

    def scatter(self, r_in: Ray, rec: "HitRecord") -> Optional[Tuple[Ray, Color]]:
        scatter_direction = rec.normal + random_unit_vector()
        scattered = Ray(rec.p, scatter_direction)
        attenuation = self.albedo
        return scattered, attenuation


class Metal(Material):
    def __init__(self, albedo: Color, fuzz: float):
        self.albedo = albedo
        self.fuzz = min(fuzz, 1.0)

    def scatter(self, r_in: Ray, rec: "HitRecord") -> Optional[Tuple[Ray, Color]]:
        reflected = reflect(unit_vector(r_in.direction), rec.normal)
        scattered = Ray(rec.p, reflected + self.fuzz * random_in_unit_sphere())
        attenuation = self.albedo
        if dot(scattered.direction, rec.normal) > 0.0:
            return scattered, attenuation
        else:
            return None


class Dielectric(Material):
    def __init__(self, ref_idx: float):
        self.ref_idx = ref_idx

    def scatter(self, r_in: Ray, rec: "HitRecord") -> Optional[Tuple[Ray, Color]]:
        attenuation = Color(1.0, 1.0, 1.0)
        etai_over_etat = (1.0 / self.ref_idx) if rec.front_face else self.ref_idx

        unit_direction = unit_vector(r_in.direction)
        cos_theta = min(dot(-unit_direction, rec.normal), 1.0)
        sin_theta = (1.0 - cos_theta**2) ** 0.5

        if etai_over_etat * sin_theta > 1.0 or random_double() < self._schlick(
            cos_theta, etai_over_etat
        ):
            # Reflect
            reflected = reflect(unit_direction, rec.normal)
            scattered = Ray(rec.p, reflected)
        else:
            # Refract
            refracted = refract(unit_direction, rec.normal, etai_over_etat)
            scattered = Ray(rec.p, refracted)

        return scattered, attenuation

    def _schlick(self, cosine: float, ref_idx: float) -> float:
        r0 = ((1.0 - ref_idx) / (1.0 + ref_idx)) ** 2
        return r0 + (1.0 - r0) * ((1.0 - cosine) ** 5)
