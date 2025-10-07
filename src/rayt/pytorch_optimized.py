import math

import torch


def dot_torch(u, v):
    return torch.dot(u, v)


def length_squared_torch(v):
    return torch.dot(v, v)


def length_torch(v):
    return torch.sqrt(length_squared_torch(v))


def unit_vector_torch(v):
    return v / length_torch(v)


def reflect_torch(v, n):
    return v - 2.0 * dot_torch(v, n) * n


def refract_torch(uv, n, etai_over_etat):
    cos_theta = dot_torch(-uv, n)
    r_out_parallel = etai_over_etat * (uv + cos_theta * n)
    r_out_perp_len = -torch.sqrt(1.0 - length_squared_torch(r_out_parallel))
    r_out_perp = r_out_perp_len * n
    return r_out_parallel + r_out_perp


def random_unit_vector_torch(device="cpu"):
    a = (torch.rand(1, device=device) * 2.0 * math.pi).item()
    z = (torch.rand(1, device=device) * 2.0 - 1.0).item()
    r = math.sqrt(1.0 - z * z)
    return torch.tensor(
        [r * math.cos(a), r * math.sin(a), z], dtype=torch.float64, device=device
    )


def random_in_unit_disk_torch(device="cpu"):
    while True:
        p = torch.rand(3, dtype=torch.float64, device=device) * 2.0 - 1.0
        p[2] = 0.0
        if length_squared_torch(p) >= 1.0:
            continue
        return p


def random_in_unit_sphere_torch(device="cpu"):
    while True:
        p = torch.rand(3, dtype=torch.float64, device=device) * 2.0 - 1.0
        if length_squared_torch(p) >= 1.0:
            continue
        return p


def sphere_hit_torch(
    ray_origin, ray_direction, sphere_center, sphere_radius, t_min, t_max, device="cpu"
):
    oc = ray_origin - sphere_center
    a = length_squared_torch(ray_direction)
    half_b = dot_torch(oc, ray_direction)
    c = length_squared_torch(oc) - sphere_radius * sphere_radius
    discriminant = half_b * half_b - a * c

    if discriminant <= 0:
        return (
            False,
            0.0,
            torch.zeros(3, dtype=torch.float64, device=device),
            torch.zeros(3, dtype=torch.float64, device=device),
            False,
        )

    root = torch.sqrt(discriminant)
    temp = (-half_b - root) / a

    if t_min < temp < t_max:
        t = temp
    else:
        temp = (-half_b + root) / a
        if t_min < temp < t_max:
            t = temp
        else:
            return (
                False,
                0.0,
                torch.zeros(3, dtype=torch.float64, device=device),
                torch.zeros(3, dtype=torch.float64, device=device),
                False,
            )

    hit_point = ray_origin + t * ray_direction
    outward_normal = (hit_point - sphere_center) / sphere_radius
    front_face = dot_torch(ray_direction, outward_normal) < 0.0
    normal = outward_normal if front_face else -outward_normal

    return True, t, hit_point, normal, front_face


def schlick_torch(cosine, ref_idx):
    r0 = ((1.0 - ref_idx) / (1.0 + ref_idx)) ** 2
    return r0 + (1.0 - r0) * ((1.0 - cosine) ** 5)


def scatter_lambertian_torch(ray_direction, hit_point, normal, device="cpu"):
    scatter_direction = normal + random_unit_vector_torch(device=device)
    return True, hit_point, scatter_direction


def scatter_metal_torch(ray_direction, hit_point, normal, fuzz, device="cpu"):
    reflected = reflect_torch(unit_vector_torch(ray_direction), normal)
    scattered_direction = reflected + fuzz * random_in_unit_sphere_torch(device=device)
    scattered = dot_torch(scattered_direction, normal) > 0.0
    return scattered, hit_point, scattered_direction


def scatter_dielectric_torch(
    ray_direction, hit_point, normal, front_face, ref_idx, device="cpu"
):
    etai_over_etat = (1.0 / ref_idx) if front_face else ref_idx
    unit_direction = unit_vector_torch(ray_direction)
    cos_theta = min(dot_torch(-unit_direction, normal), 1.0)
    sin_theta = torch.sqrt(1.0 - cos_theta * cos_theta)

    if etai_over_etat * sin_theta > 1.0 or torch.rand(1, device=device) < schlick_torch(
        cos_theta, etai_over_etat
    ):
        # Reflect
        reflected = reflect_torch(unit_direction, normal)
        scattered_direction = reflected
    else:
        # Refract
        scattered_direction = refract_torch(unit_direction, normal, etai_over_etat)

    return True, hit_point, scattered_direction


def ray_color_torch(
    ray_origin, ray_direction, spheres_data, materials_data, depth, device="cpu"
):
    if depth <= 0:
        return torch.zeros(3, dtype=torch.float64, device=device)

    current_ray_origin = ray_origin.clone()
    current_ray_direction = ray_direction.clone()
    current_color = torch.ones(3, dtype=torch.float64, device=device)

    for _ in range(depth):
        # Find closest hit
        closest_t = float("inf")
        hit_found = False
        hit_sphere_idx = -1
        hit_point = torch.zeros(3, dtype=torch.float64, device=device)
        hit_normal = torch.zeros(3, dtype=torch.float64, device=device)
        hit_front_face = False

        for i in range(spheres_data.shape[0]):
            sphere_center = spheres_data[i, :3]
            sphere_radius = spheres_data[i, 3]

            hit, t, point, normal, front_face = sphere_hit_torch(
                current_ray_origin,
                current_ray_direction,
                sphere_center,
                sphere_radius,
                0.001,
                closest_t,
                device,
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
            unit_direction = unit_vector_torch(current_ray_direction)
            t = 0.5 * (unit_direction[1] + 1.0)
            sky_color = (1.0 - t) * torch.tensor(
                [1.0, 1.0, 1.0], dtype=torch.float64, device=device
            ) + t * torch.tensor([0.5, 0.7, 1.0], dtype=torch.float64, device=device)
            return current_color * sky_color

        # Material scattering
        material = materials_data[hit_sphere_idx]
        material_type = int(material[0])

        if material_type == 0:  # Lambertian
            albedo = material[1:4]
            scattered, new_origin, new_direction = scatter_lambertian_torch(
                current_ray_direction, hit_point, hit_normal, device
            )
            if scattered:
                current_color *= albedo
                current_ray_origin = new_origin
                current_ray_direction = new_direction
            else:
                return torch.zeros(3, dtype=torch.float64, device=device)

        elif material_type == 1:  # Metal
            albedo = material[1:4]
            fuzz = material[4]
            scattered, new_origin, new_direction = scatter_metal_torch(
                current_ray_direction, hit_point, hit_normal, fuzz, device
            )
            if scattered:
                current_color *= albedo
                current_ray_origin = new_origin
                current_ray_direction = new_direction
            else:
                return torch.zeros(3, dtype=torch.float64, device=device)

        elif material_type == 2:  # Dielectric
            ref_idx = material[1]
            scattered, new_origin, new_direction = scatter_dielectric_torch(
                current_ray_direction,
                hit_point,
                hit_normal,
                hit_front_face,
                ref_idx,
                device,
            )
            current_ray_origin = new_origin
            current_ray_direction = new_direction

    return torch.zeros(3, dtype=torch.float64, device=device)


def render_pixel_torch(
    i,
    j,
    image_width,
    image_height,
    samples_per_pixel,
    camera_data,
    spheres_data,
    materials_data,
    max_depth,
    device="cpu",
):
    pixel_color = torch.zeros(3, dtype=torch.float64, device=device)

    origin = camera_data[0:3]
    lower_left_corner = camera_data[3:6]
    horizontal = camera_data[6:9]
    vertical = camera_data[9:12]
    lens_radius = camera_data[12]
    u = camera_data[13:16]
    v = camera_data[16:19]

    for _ in range(samples_per_pixel):
        u_coord = (i + torch.rand(1, device=device)) / (image_width - 1)
        v_coord = (j + torch.rand(1, device=device)) / (image_height - 1)

        rd = lens_radius * random_in_unit_disk_torch(device=device)
        offset = u * rd[0] + v * rd[1]
        ray_origin = origin + offset
        ray_direction = (
            lower_left_corner + u_coord * horizontal + v_coord * vertical - ray_origin
        )

        color = ray_color_torch(
            ray_origin,
            ray_direction,
            spheres_data,
            materials_data,
            max_depth,
            device,
        )
        pixel_color += color

    return pixel_color