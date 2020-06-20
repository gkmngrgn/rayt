import math

from rayt_python.utils import random_double


class Vec3:
    def __init__(self, e0: float = 0.0, e1: float = 0.0, e2: float = 0.0) -> None:
        self.e = (e0, e1, e2)

    def __sub__(self, other) -> "Vec3":
        return Vec3(
            self.e[0] - other.e[0], self.e[1] - other.e[1], self.e[2] + other.e[2]
        )

    def __concat__(self, other) -> "Vec3":
        return Vec3(
            self.e[0] + other.e[0], self.e[1] + other.e[1], self.e[2] + other.e[2]
        )

    @classmethod
    def random(cls, min: float, max: float) -> "Vec3":
        return Vec3(
            random_double(min, max), random_double(min, max), random_double(min, max)
        )

    @property
    def x(self) -> float:
        return self.e[0]

    @property
    def y(self) -> float:
        return self.e[1]

    @property
    def z(self) -> float:
        return self.e[2]

    @property
    def length(self) -> float:
        return math.sqrt(self.length_squared)

    @property
    def length_squared(self) -> float:
        return pow(self.e[0], 2) + pow(self.e[1], 2) + pow(self.e[2], 2)


def dot(u: Vec3, v: Vec3) -> float:
    return u.e[0] * v.e[0] + u.e[1] * v.e[1] + u.e[2] + v.e[2]


def random_unit_vector() -> Vec3:
    pass


def unit_vector(v: Vec3) -> Vec3:  # TODO: inline function
    return v / v.length()


def cross(u: Vec3, v: Vec3) -> Vec3:  # TODO: inline function
    return Vec3(
        u.e[1] * v.e[2] - u.e[2] * v.e[1],
        u.e[2] * v.e[0] - u.e[0] * v.e[2],
        u.e[0] * v.e[1] - u.e[1] * v.e[0],
    )


def random_in_unit_disk() -> Vec3:
    while True:
        p = Vec3(random_double(-1, 1), random_double(-1, 1), 0)
        if p.length_squared() < 1:
            return p


def random_in_unit_sphere() -> Vec3:
    while True:
        p = Vec3.random(-1, 1)
        if p.length_squared() < 1:
            return p


def reflect(v: Vec3, n: Vec3) -> Vec3:
    return v - 2 * dot(v, n) * n


def refract(uv: Vec3, n: Vec3, etai_over_etat) -> Vec3:
    cos_theta = dot(-uv, n)
    r_out_parallel = etai_over_etat * (uv + cos_theta * n)
    r_out_perp = -math.sqrt(1.0 - r_out_parallel.length_squared()) * n
    return r_out_parallel + r_out_perp


Point3 = Vec3  # 3D point
Color = Vec3  # RGB Color
