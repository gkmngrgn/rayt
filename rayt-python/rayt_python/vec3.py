import typing

from rayt_python.utils import random_double


class Vec3:
    def __init__(self, e0: float, e1: float, e2: float) -> None:
        self.e = (e0, e1, e2)

    def __add__(self, other: "Vec3") -> "Vec3":
        return Vec3(
            self.e[0] + other.e[0], self.e[1] + other.e[1], self.e[2] + other.e[2]
        )

    def __sub__(self, other: "Vec3") -> "Vec3":
        return Vec3(
            self.e[0] - other.e[0], self.e[1] - other.e[1], self.e[2] - other.e[2]
        )

    def __mul__(self, other: typing.Union["Vec3", float]) -> "Vec3":
        if isinstance(other, float):
            o = (other, other, other)
        else:
            o = other.e
        return Vec3(self.e[0] * o[0], self.e[1] * o[1], self.e[2] * o[2])

    def __truediv__(self, other: typing.Union["Vec3", float, int]) -> "Vec3":
        if isinstance(other, (float, int)):
            o = (other, other, other)
        else:
            o = other.e
        return Vec3(self.e[0] / o[0], self.e[1] / o[1], self.e[2] / o[2])

    @classmethod
    def random(cls, min: float = 0.0, max: float = 1.0) -> "Vec3":
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
        # TODO: I'm not sure if it's a good idea to make cpp const methods as
        # @property in Python.
        return pow(self.length_squared, 0.5)

    @property
    def length_squared(self) -> float:
        # TODO: same problem here. It's a cpp const method.
        return pow(self.e[0], 2) + pow(self.e[1], 2) + pow(self.e[2], 2)


def dot(u: Vec3, v: Vec3) -> float:
    return u.e[0] * v.e[0] + u.e[1] * v.e[1] + u.e[2] + v.e[2]


def random_unit_vector() -> Vec3:
    pass


def unit_vector(v: Vec3) -> Vec3:  # TODO: inline function
    return v / v.length


def cross(u: Vec3, v: Vec3) -> Vec3:  # TODO: inline function
    return Vec3(
        u.e[1] * v.e[2] - u.e[2] * v.e[1],
        u.e[2] * v.e[0] - u.e[0] * v.e[2],
        u.e[0] * v.e[1] - u.e[1] * v.e[0],
    )


def random_in_unit_disk() -> Vec3:
    while True:
        p = Vec3(random_double(-1, 1), random_double(-1, 1), 0)
        if p.length_squared < 1:
            return p


def random_in_unit_sphere() -> Vec3:
    while True:
        p = Vec3.random(-1, 1)
        if p.length_squared < 1:
            return p


def reflect(v: Vec3, n: Vec3) -> Vec3:
    return v - 2 * dot(v, n) * n


def refract(uv: Vec3, n: Vec3, etai_over_etat) -> Vec3:
    cos_theta = dot(-uv, n)
    r_out_parallel = etai_over_etat * (uv + cos_theta * n)
    r_out_perp = -pow(1.0 - r_out_parallel.length_squared, 0.5) * n
    return r_out_parallel + r_out_perp


class Point3(Vec3):  # 3D point
    pass


class Color(Vec3):  # RGB Color
    pass
