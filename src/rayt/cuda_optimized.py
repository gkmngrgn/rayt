import math

from numba import cuda, types
from numba.cuda.random import xoroshiro128p_uniform_float64


@cuda.jit(device=True)
def dot_cuda(u: types.float64[:], v: types.float64[:]) -> types.float64:
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


@cuda.jit(device=True)
def length_squared_cuda(v: types.float64[:]) -> types.float64:
    return v[0] * v[0] + v[1] * v[1] + v[2] * v[2]


@cuda.jit(device=True)
def length_cuda(v: types.float64[:]) -> types.float64:
    return math.sqrt(length_squared_cuda(v))


@cuda.jit(device=True)
def unit_vector_cuda(v: types.float64[:], result: types.float64[:]) -> None:
    len_v = length_cuda(v)
    result[0] = v[0] / len_v
    result[1] = v[1] / len_v
    result[2] = v[2] / len_v


@cuda.jit(device=True)
def reflect_cuda(
    v: types.float64[:], n: types.float64[:], result: types.float64[:]
) -> None:
    dot_vn = dot_cuda(v, n)
    result[0] = v[0] - 2.0 * dot_vn * n[0]
    result[1] = v[1] - 2.0 * dot_vn * n[1]
    result[2] = v[2] - 2.0 * dot_vn * n[2]


@cuda.jit(device=True)
def refract_cuda(
    uv: types.float64[:],
    n: types.float64[:],
    etai_over_etat: types.float64,
    result: types.float64[:],
) -> None:
    neg_uv = cuda.local.array(3, types.float64)
    neg_uv[0] = -uv[0]
    neg_uv[1] = -uv[1]
    neg_uv[2] = -uv[2]
    cos_theta = dot_cuda(neg_uv, n)
    cos_theta_n = cuda.local.array(3, types.float64)
    cos_theta_n[0] = cos_theta * n[0]
    cos_theta_n[1] = cos_theta * n[1]
    cos_theta_n[2] = cos_theta * n[2]

    uv_plus_cos_n = cuda.local.array(3, types.float64)
    uv_plus_cos_n[0] = uv[0] + cos_theta_n[0]
    uv_plus_cos_n[1] = uv[1] + cos_theta_n[1]
    uv_plus_cos_n[2] = uv[2] + cos_theta_n[2]

    r_out_parallel = cuda.local.array(3, types.float64)
    r_out_parallel[0] = etai_over_etat * uv_plus_cos_n[0]
    r_out_parallel[1] = etai_over_etat * uv_plus_cos_n[1]
    r_out_parallel[2] = etai_over_etat * uv_plus_cos_n[2]
    r_out_perp_len = -math.sqrt(1.0 - length_squared_cuda(r_out_parallel))

    result[0] = r_out_parallel[0] + r_out_perp_len * n[0]
    result[1] = r_out_parallel[1] + r_out_perp_len * n[1]
    result[2] = r_out_parallel[2] + r_out_perp_len * n[2]


@cuda.jit(device=True)
def random_unit_vector_cuda(
    rng_states: types.CPointer, thread_id: int, result: types.float64[:]
) -> None:
    a = xoroshiro128p_uniform_float64(rng_states, thread_id) * 2.0 * math.pi
    z = xoroshiro128p_uniform_float64(rng_states, thread_id) * 2.0 - 1.0
    r = math.sqrt(1.0 - z * z)
    result[0] = r * math.cos(a)
    result[1] = r * math.sin(a)
    result[2] = z


@cuda.jit(device=True)
def random_in_unit_sphere_cuda(
    rng_states: types.CPointer, thread_id: int, result: types.float64[:]
) -> None:
    while True:
        result[0] = xoroshiro128p_uniform_float64(rng_states, thread_id) * 2.0 - 1.0
        result[1] = xoroshiro128p_uniform_float64(rng_states, thread_id) * 2.0 - 1.0
        result[2] = xoroshiro128p_uniform_float64(rng_states, thread_id) * 2.0 - 1.0
        if length_squared_cuda(result) < 1.0:
            break


@cuda.jit(device=True)
def sphere_hit_cuda(
    ray_origin: types.float64[:],
    ray_direction: types.float64[:],
    sphere_center: types.float64[:],
    sphere_radius: types.float64,
    t_min: types.float64,
    t_max: types.float64,
    hit_point: types.float64[:],
    normal: types.float64[:],
) -> tuple[types.boolean, types.float64, types.boolean]:
    """
    Returns: hit (bool), t (float), front_face (bool)
    hit_point and normal are written in-place
    """
    oc = cuda.local.array(3, types.float64)
    oc[0] = ray_origin[0] - sphere_center[0]
    oc[1] = ray_origin[1] - sphere_center[1]
    oc[2] = ray_origin[2] - sphere_center[2]

    a = length_squared_cuda(ray_direction)
    half_b = dot_cuda(oc, ray_direction)
    c = length_squared_cuda(oc) - sphere_radius * sphere_radius
    discriminant = half_b * half_b - a * c

    if discriminant <= 0:
        return False, 0.0, False

    root = math.sqrt(discriminant)
    temp = (-half_b - root) / a

    if t_min < temp < t_max:
        t = temp
    else:
        temp = (-half_b + root) / a
        if t_min < temp < t_max:
            t = temp
        else:
            return False, 0.0, False

    hit_point[0] = ray_origin[0] + t * ray_direction[0]
    hit_point[1] = ray_origin[1] + t * ray_direction[1]
    hit_point[2] = ray_origin[2] + t * ray_direction[2]

    outward_normal = cuda.local.array(3, types.float64)
    outward_normal[0] = (hit_point[0] - sphere_center[0]) / sphere_radius
    outward_normal[1] = (hit_point[1] - sphere_center[1]) / sphere_radius
    outward_normal[2] = (hit_point[2] - sphere_center[2]) / sphere_radius

    front_face = dot_cuda(ray_direction, outward_normal) < 0.0
    if front_face:
        normal[0] = outward_normal[0]
        normal[1] = outward_normal[1]
        normal[2] = outward_normal[2]
    else:
        normal[0] = -outward_normal[0]
        normal[1] = -outward_normal[1]
        normal[2] = -outward_normal[2]

    return True, t, front_face


@cuda.jit(device=True)
def schlick_cuda(cosine: types.float64, ref_idx: types.float64) -> types.float64:
    r0 = ((1.0 - ref_idx) / (1.0 + ref_idx)) ** 2
    return r0 + (1.0 - r0) * ((1.0 - cosine) ** 5)


@cuda.jit(device=True)
def scatter_lambertian_cuda(
    ray_direction: types.float64[:],
    hit_point: types.float64[:],
    normal: types.float64[:],
    rng_states: types.CPointer,
    thread_id: int,
    new_origin: types.float64[:],
    new_direction: types.float64[:],
) -> types.boolean:
    """Returns: scattered (bool), writes new_origin and new_direction in-place"""
    scatter_direction = cuda.local.array(3, types.float64)
    random_unit_vector_cuda(rng_states, thread_id, scatter_direction)

    new_origin[0] = hit_point[0]
    new_origin[1] = hit_point[1]
    new_origin[2] = hit_point[2]

    new_direction[0] = normal[0] + scatter_direction[0]
    new_direction[1] = normal[1] + scatter_direction[1]
    new_direction[2] = normal[2] + scatter_direction[2]

    return True


@cuda.jit(device=True)
def scatter_metal_cuda(
    ray_direction: types.float64[:],
    hit_point: types.float64[:],
    normal: types.float64[:],
    fuzz: types.float64,
    rng_states: types.CPointer,
    thread_id: int,
    new_origin: types.float64[:],
    new_direction: types.float64[:],
) -> types.boolean:
    """Returns: scattered (bool), writes new_origin and new_direction in-place"""
    unit_direction = cuda.local.array(3, types.float64)
    unit_vector_cuda(ray_direction, unit_direction)

    reflected = cuda.local.array(3, types.float64)
    reflect_cuda(unit_direction, normal, reflected)

    fuzz_vector = cuda.local.array(3, types.float64)
    random_in_unit_sphere_cuda(rng_states, thread_id, fuzz_vector)

    new_origin[0] = hit_point[0]
    new_origin[1] = hit_point[1]
    new_origin[2] = hit_point[2]

    new_direction[0] = reflected[0] + fuzz * fuzz_vector[0]
    new_direction[1] = reflected[1] + fuzz * fuzz_vector[1]
    new_direction[2] = reflected[2] + fuzz * fuzz_vector[2]

    return dot_cuda(new_direction, normal) > 0.0


@cuda.jit(device=True)
def scatter_dielectric_cuda(
    ray_direction: types.float64[:],
    hit_point: types.float64[:],
    normal: types.float64[:],
    front_face: types.boolean,
    ref_idx: types.float64,
    rng_states: types.CPointer,
    thread_id: int,
    new_origin: types.float64[:],
    new_direction: types.float64[:],
) -> types.boolean:
    """Returns: scattered (bool), writes new_origin and new_direction in-place"""
    etai_over_etat = (1.0 / ref_idx) if front_face else ref_idx

    unit_direction = cuda.local.array(3, types.float64)
    unit_vector_cuda(ray_direction, unit_direction)

    neg_unit_direction = cuda.local.array(3, types.float64)
    neg_unit_direction[0] = -unit_direction[0]
    neg_unit_direction[1] = -unit_direction[1]
    neg_unit_direction[2] = -unit_direction[2]

    cos_theta = min(dot_cuda(neg_unit_direction, normal), 1.0)
    sin_theta = math.sqrt(1.0 - cos_theta * cos_theta)

    new_origin[0] = hit_point[0]
    new_origin[1] = hit_point[1]
    new_origin[2] = hit_point[2]

    if etai_over_etat * sin_theta > 1.0 or xoroshiro128p_uniform_float64(
        rng_states, thread_id
    ) < schlick_cuda(cos_theta, etai_over_etat):
        # Reflect
        reflect_cuda(unit_direction, normal, new_direction)
    else:
        # Refract
        refract_cuda(unit_direction, normal, etai_over_etat, new_direction)

    return True


@cuda.jit(device=True)
def ray_color_cuda(
    ray_origin: types.float64[:],
    ray_direction: types.float64[:],
    spheres_data: types.float64[:, :],
    materials_data: types.float64[:, :],
    depth: int,
    rng_states: types.CPointer,
    thread_id: int,
    result: types.float64[:],
) -> None:
    """
    Optimized ray color computation using CUDA
    Writes result in-place: [r, g, b]
    """
    if depth <= 0:
        result[0] = 0.0
        result[1] = 0.0
        result[2] = 0.0
        return

    current_ray_origin = cuda.local.array(3, types.float64)
    current_ray_direction = cuda.local.array(3, types.float64)
    current_color = cuda.local.array(3, types.float64)

    current_ray_origin[0] = ray_origin[0]
    current_ray_origin[1] = ray_origin[1]
    current_ray_origin[2] = ray_origin[2]

    current_ray_direction[0] = ray_direction[0]
    current_ray_direction[1] = ray_direction[1]
    current_ray_direction[2] = ray_direction[2]

    current_color[0] = 1.0
    current_color[1] = 1.0
    current_color[2] = 1.0

    for _ in range(depth):
        # Find closest hit
        closest_t = math.inf
        hit_found = False
        hit_sphere_idx = -1
        hit_point = cuda.local.array(3, types.float64)
        hit_normal = cuda.local.array(3, types.float64)
        hit_front_face = False

        for i in range(spheres_data.shape[0]):
            sphere_center = cuda.local.array(3, types.float64)
            sphere_center[0] = spheres_data[i, 0]
            sphere_center[1] = spheres_data[i, 1]
            sphere_center[2] = spheres_data[i, 2]
            sphere_radius = spheres_data[i, 3]

            temp_hit_point = cuda.local.array(3, types.float64)
            temp_normal = cuda.local.array(3, types.float64)

            hit, t, front_face = sphere_hit_cuda(
                current_ray_origin,
                current_ray_direction,
                sphere_center,
                sphere_radius,
                0.001,
                closest_t,
                temp_hit_point,
                temp_normal,
            )

            if hit and t < closest_t:
                closest_t = t
                hit_found = True
                hit_sphere_idx = i
                hit_point[0] = temp_hit_point[0]
                hit_point[1] = temp_hit_point[1]
                hit_point[2] = temp_hit_point[2]
                hit_normal[0] = temp_normal[0]
                hit_normal[1] = temp_normal[1]
                hit_normal[2] = temp_normal[2]
                hit_front_face = front_face

        if not hit_found:
            # Sky gradient
            unit_direction = cuda.local.array(3, types.float64)
            unit_vector_cuda(current_ray_direction, unit_direction)
            t = 0.5 * (unit_direction[1] + 1.0)
            sky_r = (1.0 - t) * 1.0 + t * 0.5
            sky_g = (1.0 - t) * 1.0 + t * 0.7
            sky_b = (1.0 - t) * 1.0 + t * 1.0

            result[0] = current_color[0] * sky_r
            result[1] = current_color[1] * sky_g
            result[2] = current_color[2] * sky_b
            return

        # Material scattering
        material_type = int(materials_data[hit_sphere_idx, 0])
        new_origin = cuda.local.array(3, types.float64)
        new_direction = cuda.local.array(3, types.float64)

        if material_type == 0:  # Lambertian
            albedo_r = materials_data[hit_sphere_idx, 1]
            albedo_g = materials_data[hit_sphere_idx, 2]
            albedo_b = materials_data[hit_sphere_idx, 3]

            scattered = scatter_lambertian_cuda(
                current_ray_direction,
                hit_point,
                hit_normal,
                rng_states,
                thread_id,
                new_origin,
                new_direction,
            )
            if scattered:
                current_color[0] *= albedo_r
                current_color[1] *= albedo_g
                current_color[2] *= albedo_b
                current_ray_origin[0] = new_origin[0]
                current_ray_origin[1] = new_origin[1]
                current_ray_origin[2] = new_origin[2]
                current_ray_direction[0] = new_direction[0]
                current_ray_direction[1] = new_direction[1]
                current_ray_direction[2] = new_direction[2]
            else:
                result[0] = 0.0
                result[1] = 0.0
                result[2] = 0.0
                return

        elif material_type == 1:  # Metal
            albedo_r = materials_data[hit_sphere_idx, 1]
            albedo_g = materials_data[hit_sphere_idx, 2]
            albedo_b = materials_data[hit_sphere_idx, 3]
            fuzz = materials_data[hit_sphere_idx, 4]

            scattered = scatter_metal_cuda(
                current_ray_direction,
                hit_point,
                hit_normal,
                fuzz,
                rng_states,
                thread_id,
                new_origin,
                new_direction,
            )
            if scattered:
                current_color[0] *= albedo_r
                current_color[1] *= albedo_g
                current_color[2] *= albedo_b
                current_ray_origin[0] = new_origin[0]
                current_ray_origin[1] = new_origin[1]
                current_ray_origin[2] = new_origin[2]
                current_ray_direction[0] = new_direction[0]
                current_ray_direction[1] = new_direction[1]
                current_ray_direction[2] = new_direction[2]
            else:
                result[0] = 0.0
                result[1] = 0.0
                result[2] = 0.0
                return

        elif material_type == 2:  # Dielectric
            ref_idx = materials_data[hit_sphere_idx, 1]

            scatter_dielectric_cuda(
                current_ray_direction,
                hit_point,
                hit_normal,
                hit_front_face,
                ref_idx,
                rng_states,
                thread_id,
                new_origin,
                new_direction,
            )
            # Dielectric doesn't attenuate color (white)
            current_ray_origin[0] = new_origin[0]
            current_ray_origin[1] = new_origin[1]
            current_ray_origin[2] = new_origin[2]
            current_ray_direction[0] = new_direction[0]
            current_ray_direction[1] = new_direction[1]
            current_ray_direction[2] = new_direction[2]

    result[0] = 0.0  # Exceeded max depth
    result[1] = 0.0
    result[2] = 0.0


@cuda.jit
def render_pixels_cuda(
    image_width: int,
    image_height: int,
    samples_per_pixel: int,
    camera_data: types.float64[:],
    spheres_data: types.float64[:, :],
    materials_data: types.float64[:, :],
    max_depth: int,
    rng_states: types.CPointer,
    output: types.float64[:, :, :],
) -> None:
    """
    CUDA kernel to render pixels in parallel
    output: array of shape (image_height, image_width, 3) for RGB values
    """
    i = cuda.blockIdx.x * cuda.blockDim.x + cuda.threadIdx.x
    j = cuda.blockIdx.y * cuda.blockDim.y + cuda.threadIdx.y

    if i >= image_width or j >= image_height:
        return

    thread_id = j * image_width + i

    pixel_color = cuda.local.array(3, types.float64)
    pixel_color[0] = 0.0
    pixel_color[1] = 0.0
    pixel_color[2] = 0.0

    origin = cuda.local.array(3, types.float64)
    lower_left_corner = cuda.local.array(3, types.float64)
    horizontal = cuda.local.array(3, types.float64)
    vertical = cuda.local.array(3, types.float64)

    origin[0] = camera_data[0]
    origin[1] = camera_data[1]
    origin[2] = camera_data[2]
    lower_left_corner[0] = camera_data[3]
    lower_left_corner[1] = camera_data[4]
    lower_left_corner[2] = camera_data[5]
    horizontal[0] = camera_data[6]
    horizontal[1] = camera_data[7]
    horizontal[2] = camera_data[8]
    vertical[0] = camera_data[9]
    vertical[1] = camera_data[10]
    vertical[2] = camera_data[11]

    for _ in range(samples_per_pixel):
        # Add random sampling
        u_coord = (i + xoroshiro128p_uniform_float64(rng_states, thread_id)) / (
            image_width - 1
        )
        v_coord = (j + xoroshiro128p_uniform_float64(rng_states, thread_id)) / (
            image_height - 1
        )

        # Simple camera ray (ignoring depth of field for now in this optimization)
        ray_direction = cuda.local.array(3, types.float64)
        ray_direction[0] = (
            lower_left_corner[0]
            + u_coord * horizontal[0]
            + v_coord * vertical[0]
            - origin[0]
        )
        ray_direction[1] = (
            lower_left_corner[1]
            + u_coord * horizontal[1]
            + v_coord * vertical[1]
            - origin[1]
        )
        ray_direction[2] = (
            lower_left_corner[2]
            + u_coord * horizontal[2]
            + v_coord * vertical[2]
            - origin[2]
        )

        color = cuda.local.array(3, types.float64)
        ray_color_cuda(
            origin,
            ray_direction,
            spheres_data,
            materials_data,
            max_depth,
            rng_states,
            thread_id,
            color,
        )

        pixel_color[0] += color[0]
        pixel_color[1] += color[1]
        pixel_color[2] += color[2]

    # Store result (note: j is flipped for correct image orientation)
    output[image_height - 1 - j, i, 0] = pixel_color[0]
    output[image_height - 1 - j, i, 1] = pixel_color[1]
    output[image_height - 1 - j, i, 2] = pixel_color[2]
