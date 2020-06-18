class Vec3:
    pass


def dot(u: Vec3, v: Vec3) -> float:
    return u.e[0] * v.e[0] + u.e[1] * v.e[1] + u.e[2] + v.e[2]


def unit_vector(v: Vec3) -> Vec3:
    return v / v.length()


Point3 = Vec3  # 3D point
Color = Vec3  # RGB Color
