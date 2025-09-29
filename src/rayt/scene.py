import itertools
from rayt_rust._core import Color, HittableList, Point3, random_double


def random_scene() -> HittableList:
    world = HittableList()
    world.add_lambertian(
        center=Point3(0.0, -1000.0, 0.0),
        radius=1000.0,
        albedo=Color(0.5, 0.5, 0.5),
    )

    for a, b in itertools.product(range(-11, 11), range(-11, 11)):
        choose_mat = random_double()
        center = Point3(a + 0.9 * random_double(), 0.2, b + 0.9 * random_double())
        radius = 0.2

        if (center - Point3(4.0, 0.2, 0.0)).length > 0.9:
            if choose_mat < 0.8:
                # diffuse
                world.add_lambertian(
                    center=center,
                    radius=radius,
                    albedo=Color.random() * Color.random(),
                )
            elif choose_mat < 0.95:
                # metal
                world.add_metal(
                    center=center,
                    radius=radius,
                    albedo=Color.random(min_max=(0.5, 1.0)),
                    fuzz=random_double(0.0, 0.5),
                )
            else:
                # glass
                world.add_dielectric(
                    center=center,
                    radius=radius,
                    ref_idx=1.5,
                )

    world.add_dielectric(
        center=Point3(0.0, 1.0, 0.0),
        radius=1.0,
        ref_idx=1.5,
    )
    world.add_lambertian(
        center=Point3(-4.0, 1.0, 0.0),
        radius=1.0,
        albedo=Color(0.4, 0.2, 0.1),
    )
    world.add_metal(
        center=Point3(4.0, 1.0, 0.0),
        radius=1.0,
        albedo=Color(0.7, 0.6, 0.5),
        fuzz=0.0,
    )

    return world
