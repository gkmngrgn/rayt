use rayt::{
    camera::Camera,
    color::write_color,
    hittable::Hittable,
    hittable_list::HittableList,
    material::{Material, Scatter},
    ray::Ray,
    sphere::Sphere,
    utils::INFINITY,
    vec3::{unit_vector, Color, Point3, Vec3},
};

#[macro_use]
extern crate rayt;

fn ray_color(r: &Ray, world: &HittableList, depth: usize) -> Color {
    // FIXME: don't use recursive here. take a look at the Python code.
    if depth == 0 {
        return Color::from([0.0, 0.0, 0.0]);
    }

    if let Some(rec) = world.hit(r, 0.001, INFINITY) {
        if let Some((scattered, attenuation)) = rec.material.scatter(r, rec) {
            let r_color: Color = ray_color(&scattered, world, depth - 1);
            return attenuation * r_color;
        }
        return Color::from([0.0, 0.0, 0.0]);
    }

    let unit_direction = unit_vector(r.direction);
    let t = 0.5 * (unit_direction.y + 1.0);
    (1.0 - t) * Color::from([1.0, 1.0, 1.0]) + t * Color::from([0.5, 0.7, 1.0])
}

fn random_scene() -> HittableList {
    let mut world = HittableList::default();
    let ground_material = Material::new_lambertian(Color::from([0.5, 0.5, 0.5]));
    world.add(Sphere::new(
        Point3::from([0.0, -1000.0, 0.0]),
        1000.0,
        ground_material,
    ));

    for a in -11..11 {
        for b in -11..11 {
            let choose_mat = random_double!();
            let center = Point3::from([
                a as f64 + 0.9 * random_double!(),
                0.2,
                b as f64 + 0.9 * random_double!(),
            ]);

            if (center - Point3::from([4.0, 0.2, 0.0])).length() > 0.9 {
                let sphere_material = if choose_mat < 0.8 {
                    let albedo = Color::random(None) * Color::random(None);
                    Material::new_lambertian(albedo)
                } else if choose_mat < 0.95 {
                    let albedo = Color::random(Some([0.5, 1.0]));
                    let fuzz = random_double!(0.0, 0.5);
                    Material::new_metal(albedo, fuzz)
                } else {
                    Material::new_dielectric(1.5)
                };
                world.add(Sphere::new(center, 0.2, sphere_material));
            }
        }
    }

    let material_1 = Material::new_dielectric(1.5);
    world.add(Sphere::new(Point3::from([0.0, 1.0, 0.0]), 1.0, material_1));

    let material_2 = Material::new_lambertian(Color::from([0.4, 0.2, 0.1]));
    world.add(Sphere::new(Point3::from([-4.0, 1.0, 0.0]), 1.0, material_2));

    let material_3 = Material::new_metal(Color::from([0.7, 0.6, 0.5]), 0.0);
    world.add(Sphere::new(Point3::from([4.0, 1.0, 0.0]), 1.0, material_3));

    world
}

fn main() {
    const ASPECT_RATIO: f64 = 16.0 / 9.0;
    const IMAGE_WIDTH: u32 = 300;
    const IMAGE_HEIGHT: u32 = ((IMAGE_WIDTH as f64) / ASPECT_RATIO) as u32;
    const SAMPLES_PER_PIXEL: usize = 20;
    const MAX_DEPTH: usize = 50;

    println!("P3\n{} {}\n255\n", IMAGE_WIDTH, IMAGE_HEIGHT);

    let world = random_scene();
    let lookfrom = Point3::from([13.0, 2.0, 3.0]);
    let lookat = Point3::from([0.0, 0.0, 0.0]);
    let vup = Vec3::from([0.0, 1.0, 0.0]);
    let dist_to_focus = 10.0;
    let aperture = 0.1;

    let cam = Camera::new(
        lookfrom,
        lookat,
        vup,
        20.0,
        ASPECT_RATIO,
        aperture,
        dist_to_focus,
    );

    for j in (0..IMAGE_HEIGHT).rev() {
        eprint!("\rScanlines remaining: {} ", j);

        for i in 0..IMAGE_WIDTH {
            let pixel_color = (1..=SAMPLES_PER_PIXEL)
                .map(|_| {
                    let u = (i as f64 + random_double!()) / (IMAGE_WIDTH - 1) as f64;
                    let v = (j as f64 + random_double!()) / (IMAGE_HEIGHT - 1) as f64;
                    let r = cam.get_ray(u, v);
                    ray_color(&r, &world, MAX_DEPTH)
                })
                .fold(Color::from([0.0, 0.0, 0.0]), |sum, c| sum + c);
            write_color(pixel_color, SAMPLES_PER_PIXEL);
        }
    }

    eprintln!("\nDone.");
}
