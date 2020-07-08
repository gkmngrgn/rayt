import math
import typing

from rayt_python.utils import random_double


class Vec3:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __eq__(self, other: typing.Union["Vec3", None]) -> bool:
        if other is None:
            return False
        return all([self.x == other.x, self.y == other.y, self.z == other.z])

    def __add__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: typing.Union["Vec3", float]) -> "Vec3":
        if isinstance(other, float):
            x, y, z = self.x * other, self.y * other, self.z * other
        else:
            x, y, z = (self.x * other.x, self.y * other.y, self.z * other.z)
        return Vec3(x, y, z)

    def __rmul__(self, other: typing.Union["Vec3", float]) -> "Vec3":
        return self.__mul__(other)

    def __neg__(self) -> "Vec3":
        return Vec3(-self.x, -self.y, -self.z)

    def __truediv__(self, other: typing.Union["Vec3", float]) -> "Vec3":
        if isinstance(other, float):
            return self.__mul__(1 / other)
        return Vec3(self.x / other.x, self.y / other.y, self.z / other.z)

    @classmethod
    def random(cls, min: float = 0.0, max: float = 1.0) -> "Vec3":
        return Vec3(
            random_double(min, max), random_double(min, max), random_double(min, max)
        )

    @property
    def length(self) -> float:
        return pow(self.length_squared, 0.5)

    @property
    def length_squared(self) -> float:
        return pow(self.x, 2) + pow(self.y, 2) + pow(self.z, 2)


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


class Point3(Vec3):  # 3D point
    pass


class Color(Vec3):  # RGB Color
    pass
