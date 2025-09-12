import math

import numpy as np
from numba import jit


@jit(nopython=True)
def dot_numba(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


@jit(nopython=True)
def length_squared_numba(v):
    return v[0] ** 2 + v[1] ** 2 + v[2] ** 2


@jit(nopython=True)
def length_numba(v):
    return math.sqrt(length_squared_numba(v))


@jit(nopython=True)
def unit_vector_numba(v):
    len_v = length_numba(v)
    return np.array([v[0] / len_v, v[1] / len_v, v[2] / len_v])


@jit(nopython=True)
def reflect_numba(v, n):
    dot_vn = dot_numba(v, n)
    return np.array(
        [
            v[0] - 2.0 * dot_vn * n[0],
            v[1] - 2.0 * dot_vn * n[1],
            v[2] - 2.0 * dot_vn * n[2],
        ]
    )


@jit(nopython=True)
def refract_numba(uv, n, etai_over_etat):
    cos_theta = dot_numba(-uv, n)
    r_out_parallel = etai_over_etat * (uv + cos_theta * n)
    r_out_perp_len = -math.sqrt(1.0 - length_squared_numba(r_out_parallel))
    r_out_perp = r_out_perp_len * n
    return r_out_parallel + r_out_perp


@jit(nopython=True)
def random_unit_vector_numba():
    a = np.random.uniform(0.0, 2.0 * math.pi)
    z = np.random.uniform(-1.0, 1.0)
    r = math.sqrt(1.0 - z * z)
    return np.array([r * math.cos(a), r * math.sin(a), z])


@jit(nopython=True)
def random_in_unit_disk_numba():
    """Generate random point in unit disk for depth of field"""
    while True:
        p = np.array(
            [
                np.random.uniform(-1.0, 1.0),
                np.random.uniform(-1.0, 1.0),
                0.0
            ]
        )
        if length_squared_numba(p) >= 1.0:
            continue
        return p


@jit(nopython=True)
def random_in_unit_sphere_numba():
    while True:
        p = np.array(
            [
                np.random.uniform(-1.0, 1.0),
                np.random.uniform(-1.0, 1.0),
                np.random.uniform(-1.0, 1.0),
            ]
        )
        if length_squared_numba(p) >= 1.0:
            continue
        return p


@jit(nopython=True)
def sphere_hit_numba(
    ray_origin, ray_direction, sphere_center, sphere_radius, t_min, t_max
):
    oc = ray_origin - sphere_center
    a = length_squared_numba(ray_direction)
    half_b = dot_numba(oc, ray_direction)
    c = length_squared_numba(oc) - sphere_radius * sphere_radius
    discriminant = half_b * half_b - a * c

    if discriminant <= 0:
        return False, 0.0, np.zeros(3), np.zeros(3), False

    root = math.sqrt(discriminant)
    temp = (-half_b - root) / a

    if t_min < temp < t_max:
        t = temp
    else:
        temp = (-half_b + root) / a
        if t_min < temp < t_max:
            t = temp
        else:
            return False, 0.0, np.zeros(3), np.zeros(3), False

    hit_point = ray_origin + t * ray_direction
    outward_normal = (hit_point - sphere_center) / sphere_radius
    front_face = dot_numba(ray_direction, outward_normal) < 0.0
    normal = outward_normal if front_face else -outward_normal

    return True, t, hit_point, normal, front_face


@jit(nopython=True)
def schlick_numba(cosine, ref_idx):
    r0 = ((1.0 - ref_idx) / (1.0 + ref_idx)) ** 2
    return r0 + (1.0 - r0) * ((1.0 - cosine) ** 5)


@jit(nopython=True)
def scatter_lambertian_numba(ray_direction, hit_point, normal):
    scatter_direction = normal + random_unit_vector_numba()
    return True, hit_point, scatter_direction


@jit(nopython=True)
def scatter_metal_numba(ray_direction, hit_point, normal, fuzz):
    reflected = reflect_numba(unit_vector_numba(ray_direction), normal)
    scattered_direction = reflected + fuzz * random_in_unit_sphere_numba()
    scattered = dot_numba(scattered_direction, normal) > 0.0
    return scattered, hit_point, scattered_direction


@jit(nopython=True)
def scatter_dielectric_numba(ray_direction, hit_point, normal, front_face, ref_idx):
    etai_over_etat = (1.0 / ref_idx) if front_face else ref_idx
    unit_direction = unit_vector_numba(ray_direction)
    cos_theta = min(dot_numba(-unit_direction, normal), 1.0)
    sin_theta = math.sqrt(1.0 - cos_theta * cos_theta)

    if etai_over_etat * sin_theta > 1.0 or np.random.random() < schlick_numba(
        cos_theta, etai_over_etat
    ):
        # Reflect
        reflected = reflect_numba(unit_direction, normal)
        scattered_direction = reflected
    else:
        # Refract
        scattered_direction = refract_numba(unit_direction, normal, etai_over_etat)

    return True, hit_point, scattered_direction


@jit(nopython=True)
def ray_color_numba(ray_origin, ray_direction, spheres_data, materials_data, depth):
    if depth <= 0:
        return np.array([0.0, 0.0, 0.0])

    current_ray_origin = ray_origin.copy()
    current_ray_direction = ray_direction.copy()
    current_color = np.array([1.0, 1.0, 1.0])

    for _ in range(depth):
        # Find closest hit
        closest_t = np.inf
        hit_found = False
        hit_sphere_idx = -1
        hit_point = np.zeros(3)
        hit_normal = np.zeros(3)
        hit_front_face = False

        for i in range(spheres_data.shape[0]):
            sphere_center = spheres_data[i, :3]
            sphere_radius = spheres_data[i, 3]

            hit, t, point, normal, front_face = sphere_hit_numba(
                current_ray_origin,
                current_ray_direction,
                sphere_center,
                sphere_radius,
                0.001,
                closest_t,
            )

            if hit and t < closest_t:
                closest_t = t
                hit_found = True
                hit_sphere_idx = i
                hit_point = point
                hit_normal = normal
                hit_front_face = front_face

        if not hit_found:
            # Sky gradient
            unit_direction = unit_vector_numba(current_ray_direction)
            t = 0.5 * (unit_direction[1] + 1.0)
            sky_color = (1.0 - t) * np.array([1.0, 1.0, 1.0]) + t * np.array(
                [0.5, 0.7, 1.0]
            )
            return current_color * sky_color

        # Material scattering
        material = materials_data[hit_sphere_idx]
        material_type = int(material[0])

        if material_type == 0:  # Lambertian
            albedo = material[1:4]
            scattered, new_origin, new_direction = scatter_lambertian_numba(
                current_ray_direction, hit_point, hit_normal
            )
            if scattered:
                current_color *= albedo
                current_ray_origin = new_origin
                current_ray_direction = new_direction
            else:
                return np.array([0.0, 0.0, 0.0])

        elif material_type == 1:  # Metal
            albedo = material[1:4]
            fuzz = material[4]
            scattered, new_origin, new_direction = scatter_metal_numba(
                current_ray_direction, hit_point, hit_normal, fuzz
            )
            if scattered:
                current_color *= albedo
                current_ray_origin = new_origin
                current_ray_direction = new_direction
            else:
                return np.array([0.0, 0.0, 0.0])

        elif material_type == 2:  # Dielectric
            ref_idx = material[1]
            scattered, new_origin, new_direction = scatter_dielectric_numba(
                current_ray_direction, hit_point, hit_normal, hit_front_face, ref_idx
            )
            # Dielectric doesn't attenuate color (white)
            current_ray_origin = new_origin
            current_ray_direction = new_direction

    return np.array([0.0, 0.0, 0.0])  # Exceeded max depth


@jit(nopython=True)
def render_pixel_numba(
    i,
    j,
    image_width,
    image_height,
    samples_per_pixel,
    camera_data,
    spheres_data,
    materials_data,
    max_depth,
):
    pixel_color = np.array([0.0, 0.0, 0.0])

    origin = camera_data[0:3]
    lower_left_corner = camera_data[3:6]
    horizontal = camera_data[6:9]
    vertical = camera_data[9:12]
    lens_radius = camera_data[12]
    u = camera_data[13:16]
    v = camera_data[16:19]

    for _ in range(samples_per_pixel):
        # Add random sampling
        u_coord = (i + np.random.random()) / (image_width - 1)
        v_coord = (j + np.random.random()) / (image_height - 1)

        # Depth of field ray generation
        rd = lens_radius * random_in_unit_disk_numba()
        offset = u * rd[0] + v * rd[1]
        ray_origin = origin + offset
        ray_direction = (
            lower_left_corner + u_coord * horizontal + v_coord * vertical - ray_origin
        )

        color = ray_color_numba(
            ray_origin, ray_direction, spheres_data, materials_data, max_depth
        )
        pixel_color += color

    return pixel_color
