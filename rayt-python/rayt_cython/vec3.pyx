from __future__ import print_function
from libc.math cimport sqrt, pow


cdef class Vec3:
    cdef double x, y, z

    def __cinit__(self, double x, double y, double z):
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

    def __sub__(Vec3 x, Vec3 y):
        cdef Vec3 result = Vec3(x.x - y.x, x.y - y.y, x.z - y.z)
        return result

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
