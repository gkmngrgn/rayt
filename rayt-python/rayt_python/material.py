import typing

from rayt_python.ray import Ray
from rayt_python.utils import random_double
from rayt_python.vec3 import (
    Color,
    dot,
    random_in_unit_sphere,
    random_unit_vector,
    reflect,
    refract,
    unit_vector,
)

if typing.TYPE_CHECKING:
    from rayt_python.hittable import HitRecord


class Material:
    def scatter(self, r_in: Ray, rec: "HitRecord") -> typing.NoReturn:
        raise NotImplementedError


class Lambertian(Material):
    def __init__(self, albedo: Color) -> None:
        self.albedo = albedo

    def scatter(
        self, r_in: Ray, rec: "HitRecord"
    ) -> typing.Union[typing.Tuple[Ray, Color], None]:
        scatter_direction = rec.normal + random_unit_vector()
        scattered = Ray(origin=rec.p, direction=scatter_direction)
        return scattered, self.albedo


class Metal(Material):
    def __init__(self, a: Color, f: float) -> None:
        self.albedo = a
        self.fuzz = f if f < 1 else 1

    def scatter(
        self, r_in: Ray, rec: "HitRecord"
    ) -> typing.Union[typing.Tuple[Ray, Color], None]:
        reflected = reflect(unit_vector(r_in.direction), rec.normal)
        scattered = Ray(rec.p, reflected + self.fuzz * random_in_unit_sphere())
        if dot(scattered.direction, rec.normal) > 0:
            return scattered, self.albedo
        return None, None


class Dielectric(Material):
    def __init__(self, ri: float) -> None:
        self.ref_idx = ri

    def scatter(
        self, r_in: Ray, rec: "HitRecord"
    ) -> typing.Union[typing.Tuple[Ray, Color], None]:
        attenuation = Color(1.0, 1.0, 1.0)
        etai_over_etat = 1.0 / self.ref_idx if rec.front_face is True else self.ref_idx
        unit_direction = unit_vector(r_in.direction)
        cos_theta = min(dot(-unit_direction, rec.normal), 1.0)
        sin_theta = pow(1.0 - pow(cos_theta, 2), 0.5)
        reflect_prob = schlick(cos_theta, etai_over_etat)

        if etai_over_etat * sin_theta > 1.0 or random_double() < reflect_prob:
            direction = reflect(unit_direction, rec.normal)
        else:
            direction = refract(unit_direction, rec.normal, etai_over_etat)

        scattered = Ray(rec.p, direction)
        return scattered, attenuation


def schlick(cosine: float, ref_idx: float) -> float:
    r0 = pow((1 - ref_idx) / (1 + ref_idx), 2)
    return r0 + (1 - r0) * pow((1 - cosine), 5)
