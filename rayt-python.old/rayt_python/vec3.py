import math

from rayt_python.utils import random_double
from rayt_python.vec3_types import Vec3


def dot(u: Vec3, v: Vec3) -> float:
    return u.x * v.x + u.y * v.y + u.z * v.z


def random_unit_vector() -> Vec3:
    a = random_double(0.0, 2 * math.pi)
    z = random_double(-1, 1)
    r = pow(1 - pow(z, 2), 0.5)
    return Vec3(r * math.cos(a), r * math.sin(a), z)


def unit_vector(v: Vec3) -> Vec3:
    return v / v.length


def cross(u: Vec3, v: Vec3) -> Vec3:
    return Vec3(u.y * v.z - u.z * v.y, u.z * v.x - u.x * v.z, u.x * v.y - u.y * v.x)


def random_in_unit_disk() -> Vec3:
    while True:
        p = Vec3(random_double(-1, 1), random_double(-1, 1), 0)
        if p.length_squared >= 1:
            continue
        return p


def random_in_unit_sphere() -> Vec3:
    while True:
        p = Vec3.random(-1, 1)
        if p.length_squared >= 1:
            continue
        return p


def reflect(v: Vec3, n: Vec3) -> Vec3:
    return v - 2 * dot(v, n) * n


def refract(uv: Vec3, n: Vec3, etai_over_etat: float) -> Vec3:
    cos_theta = dot(-uv, n)
    r_out_parallel = etai_over_etat * (uv + cos_theta * n)
    r_out_perp = -pow(1.0 - r_out_parallel.length_squared, 0.5) * n
    return r_out_parallel + r_out_perp
