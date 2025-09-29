import sys
from rayt_rust._core import Camera, HittableList, get_color, random_double, ray_color, Color


def render_with_rust(
    world: HittableList,
    camera: Camera,
    image_width: int,
    image_height: int,
    samples_per_pixel: int,
    max_depth: int,
) -> None:
    print("P3")
    print(f"{image_width} {image_height}")
    print("255")

    for j in range(image_height, 0, -1):
        print(f"\rScanlines remaining: {j}", end=" ", file=sys.stderr)

        for i in range(image_width):
            pixel_color = Color(0.0, 0.0, 0.0)

            for _ in range(1, samples_per_pixel + 1):
                u = (i + random_double()) / (image_width - 1)
                v = (j + random_double()) / (image_height - 1)
                ray = camera.get_ray(u, v)
                pixel_color += ray_color(ray, world, max_depth)

            print(get_color(pixel_color, samples_per_pixel))

    print("\nDone.", file=sys.stderr)
