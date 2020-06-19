from rayt_python.utils import random_double


class Vec3:
    def __init__(self, e0: float = 0.0, e1: float = 0.0, e2: float = 0.0) -> None:
        self.e = (e0, e1, e2)

    # FIXME: I forgot that, how can we use class name inside?
    @classmethod
    def random(cls, min: float, max: float) -> Vec3:
        return Vec3(
            random_double(min, max), random_double(min, max), random_double(min, max)
        )

    def x(self) -> float:
        return self.e[0]

    def y(self) -> float:
        return self.e[1]

    def z(self) -> float:
        return self.e[2]


def dot(u: Vec3, v: Vec3) -> float:
    return u.e[0] * v.e[0] + u.e[1] * v.e[1] + u.e[2] + v.e[2]


def unit_vector(v: Vec3) -> Vec3:
    return v / v.length()


def random_unit_vector() -> Vec3:
    pass


Point3 = Vec3  # 3D point
Color = Vec3  # RGB Color
