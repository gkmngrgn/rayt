from __future__ import print_function

from libc.math cimport pow, sqrt
from libc.stdlib cimport RAND_MAX, rand


cdef class Vec3:
    cdef public double x, y, z

    def __init__(self, double x, double y, double z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vec3({self.x}, {self.y}, {self.z})"

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __eq__(self, Vec3 y):
        cdef bint is_equal = self.x == y.x and self.y == y.y and self.z == y.z
        return is_equal

    def __add__(Vec3 x, Vec3 y):
        cdef Vec3 result = Vec3(x.x + y.x, x.y + y.y, x.z + y.z)
        return result

    def __iadd__(Vec3 self, Vec3 x):
        self.x += x.x
        self.y += x.y
        self.z += x.z
        return self

    def __sub__(Vec3 x, Vec3 y):
        cdef Vec3 result = Vec3(x.x - y.x, x.y - y.y, x.z - y.z)
        return result

    def __isub__(Vec3 self, Vec3 x):
        self.x -= x.x
        self.y -= x.y
        self.z -= x.z
        return self

    def __mul__(x, y):
        cdef Vec3 result
        if isinstance(x, float):
            result = Vec3((<Vec3>y).x * x, (<Vec3>y).y * x, (<Vec3>y).z * x)
        elif isinstance(y, float):
            result = Vec3((<Vec3>x).x * y, (<Vec3>x).y * y, (<Vec3>x).z * y)
        else:
            result = Vec3(
                (<Vec3>x).x * (<Vec3>y).x,
                (<Vec3>x).y * (<Vec3>y).y,
                (<Vec3>x).z * (<Vec3>y).z,
            )
        return result

    def __imul__(Vec3 self, x):
        cdef float e1, e2, e3
        if isinstance(x, float):
            (e1, e2, e3) = (x, x, x)
        else:
            (e1, e2, e3) = (x.x, x.y, x.z)

        self.x *= e1
        self.y *= e2
        self.z *= e3
        return self

    def __truediv__(x, y):
        cdef Vec3 result
        if isinstance(x, float):
            result = Vec3.__mul__(1 / x, y)
        elif isinstance(y, float):
            result = Vec3.__mul__(x, 1 / y)
        else:
            result = Vec3(
                (<Vec3>x).x / (<Vec3>y).x,
                (<Vec3>x).y / (<Vec3>y).y,
                (<Vec3>x).z / (<Vec3>y).z,
            )
        return result

    def __itruediv__(Vec3 self, x):
        cdef Vec3 result
        if isinstance(x, float):
            self.__imul__(self, 1 / x)
        else:
            self.x /= x.x
            self.y /= x.y
            self.z /= x.z
        return self

    @classmethod
    def random(cls, double min=0.0, double max=1.0):
        cdef Vec3 vec3 = Vec3(
            random_double(min, max),
            random_double(min, max),
            random_double(min, max),
        )
        return vec3

    @property
    def length(self):
        return sqrt(self.length_squared)

    @property
    def length_squared(self):
        return pow(self.x, 2) + pow(self.y, 2) + pow(self.z, 2)


cdef class Point3(Vec3):  # 3D point
    def __repr__(self):
        return f"Point3({self.x}, {self.y}, {self.z})"

cdef class Color(Vec3):  # RGB color
    def __repr__(self):
        return f"Color({self.x}, {self.y}, {self.z})"


cdef random_double(double min, double max):
    # TODO: it's a repeated function. there's a DRY problem.
    #       can we merge this func with utils.py/random_double()?
    cdef double div = RAND_MAX / (max - min)
    cdef double result = min + (rand() / div)
    return result
