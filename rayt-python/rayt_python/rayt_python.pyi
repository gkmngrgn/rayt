# vector classes
class Vec3:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float) -> None: ...
    def __add__(self, other: Vec3 | float) -> Vec3: ...
    def __sub__(self, other: Vec3 | float) -> Vec3: ...
    def __mul__(self, other: Vec3 | float) -> Vec3: ...
    @staticmethod
    def random(min_max: tuple[float, float] | None = None) -> Vec3: ...
    @property
    def length(self) -> float: ...

# camera
class Camera:
    def __init__(
        self,
        lookfrom: Vec3,
        lookat: Vec3,
        vup: Vec3,
        vfov: float,
        aspect_ratio: float,
        aperture: float,
        focus_dist: float,
    ) -> None: ...
    def get_ray(self, s: float, t: float) -> Ray: ...

# hittable
class HittableList:
    def __init__(self) -> None: ...
    def add_lambertian(self, center: Vec3, radius: float, albedo: Vec3) -> None: ...
    def add_metal(
        self, center: Vec3, radius: float, albedo: Vec3, fuzz: float
    ) -> None: ...
    def add_dielectric(self, center: Vec3, radius: float, ref_idx: float) -> None: ...

# materials
class Lambertian:
    def __init__(self, albedo: Vec3) -> None: ...

class Metal:
    def __init__(self, albedo: Vec3, fuzz: float) -> None: ...

class Dielectric:
    def __init__(self, ref_idx: float) -> None: ...

# ray
class Ray:
    origin: Vec3
    direction: Vec3

    def __init__(self, origin: Vec3, direction: Vec3) -> None: ...

# utils, functions
def random_double(min: float = 0.0, max: float = 1.0) -> float: ...
def unit_vector(v: Vec3) -> Vec3: ...
def get_color(pixel_color: Vec3, samples_per_pixel: int) -> str: ...
def ray_color(ray: Ray, world: HittableList, depth: int) -> Vec3: ...