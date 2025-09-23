import math
import random
from typing import List, Optional, Union


class Vec3:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def random(
        cls, min_max: Optional[Union[List[float], tuple[float, float]]] = None
    ) -> "Vec3":
        if min_max is None:
            return cls(random.random(), random.random(), random.random())
        else:
            min_val, max_val = min_max
            return cls(
                random.uniform(min_val, max_val),
                random.uniform(min_val, max_val),
                random.uniform(min_val, max_val),
            )

    @property
    def length(self) -> float:
        return math.sqrt(self.length_squared)

    @property
    def length_squared(self) -> float:
        return self.x**2 + self.y**2 + self.z**2

    def __add__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: Union["Vec3", float]) -> "Vec3":
        if isinstance(other, Vec3):
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Vec3(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other: float) -> "Vec3":
        return self * other

    def __truediv__(self, other: Union["Vec3", float]) -> "Vec3":
        if isinstance(other, Vec3):
            return Vec3(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            return self * (1.0 / other)

    def __neg__(self) -> "Vec3":
        return Vec3(-self.x, -self.y, -self.z)

    def __iadd__(self, other: "Vec3") -> "Vec3":
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __imul__(self, other: Union["Vec3", float]) -> "Vec3":
        if isinstance(other, Vec3):
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
        else:
            self.x *= other
            self.y *= other
            self.z *= other
        return self

    def __repr__(self) -> str:
        return f"Vec3({self.x}, {self.y}, {self.z})"


# Type aliases
Point3 = Vec3
Color = Vec3


# Utility functions
def dot(u: Vec3, v: Vec3) -> float:
    return u.x * v.x + u.y * v.y + u.z * v.z


def cross(u: Vec3, v: Vec3) -> Vec3:
    return Vec3(u.y * v.z - u.z * v.y, u.z * v.x - u.x * v.z, u.x * v.y - u.y * v.x)


def unit_vector(v: Vec3) -> Vec3:
    return v / v.length


def random_in_unit_sphere() -> Vec3:
    while True:
        p = Vec3.random([-1.0, 1.0])
        if p.length_squared >= 1.0:
            continue
        return p


def random_unit_vector() -> Vec3:
    a = random.uniform(0.0, 2.0 * math.pi)
    z = random.uniform(-1.0, 1.0)
    r = math.sqrt(1.0 - z**2)
    return Vec3(r * math.cos(a), r * math.sin(a), z)


def reflect(v: Vec3, n: Vec3) -> Vec3:
    return v - 2.0 * dot(v, n) * n


def refract(uv: Vec3, n: Vec3, etai_over_etat: float) -> Vec3:
    cos_theta = dot(-uv, n)
    r_out_parallel = etai_over_etat * (uv + cos_theta * n)
    r_out_perp = -math.sqrt(1.0 - r_out_parallel.length_squared) * n
    return r_out_parallel + r_out_perp


def random_double(min_val: float = 0.0, max_val: float = 1.0) -> float:
    return random.uniform(min_val, max_val)
