from __future__ import print_function


cdef class Vec3:
    cdef double x, y, z

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def print_vec3(self):
        print("Vec3 {", self.x, self.y, self.z, "}")
