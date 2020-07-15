from __future__ import print_function

cdef class Vec3:
    cdef double x, y, z

    def __init__(self, double x, double y, double z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, Vec3 other):
        cdef Vec3 result = Vec3(
            (<Vec3>self).x + (<Vec3>other).x,
            (<Vec3>self).y + (<Vec3>other).y,
            (<Vec3>self).z + (<Vec3>other).z,
        )
        return result
