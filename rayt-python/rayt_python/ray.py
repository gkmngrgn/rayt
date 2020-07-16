from rayt_python.vec3_types import Point3, Vec3


class Ray:
    def __init__(self, origin: Point3, direction: Vec3) -> None:
        self.origin = origin
        self.direction = direction

    def at(self, t: float) -> Point3:
        return self.origin + self.direction * t
