mod camera;
mod color;
mod hittable;
mod hittable_list;
mod material;
mod ray;
mod sphere;
mod utils;
mod vec3;

use crate::{
    camera::Camera,
    color::write_color,
    hittable_list::HittableList,
    ray::Ray,
    sphere::Sphere,
    utils::INFINITY,
    vec3::{unit_vector, Color, Point3, Vec3},
};
use hittable::Hittable;
use material::{Dielectric, Lambertian, Metal};

#[macro_use]
extern crate itertools;

fn ray_color(r: &Ray, world: &HittableList, depth: usize) -> Color {
    // FIXME: don't use recursive here. take a look at the Python code.
    if depth <= 0 {
        return Color::from([0.0, 0.0, 0.0]);
    }

    if let Some(rec) = world.hit(r, 0.001, INFINITY) {
        if let Some((scattered, attenuation)) = rec.material.scatter(r, &rec) {
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
    let ground_material = Lambertian::new(Color::from([0.5, 0.5, 0.5]));
    world.add(Sphere::new(
        Point3::from([0.0, -1000.0, 0.0]),
        1000.0,
        Box::new(ground_material),
    ));

    // TODO: add small materials here.

    let material_1 = Dielectric::new(1.5);
    world.add(Sphere::new(
        Point3::from([0.0, 1.0, 0.0]),
        1.0,
        Box::new(material_1),
    ));

    let material_2 = Lambertian::new(Color::from([0.4, 0.2, 0.1]));
    world.add(Sphere::new(
        Point3::from([-4.0, 1.0, 0.0]),
        1.0,
        Box::new(material_2),
    ));

    let material_3 = Metal::new(Color::from([0.7, 0.6, 0.5]), 0.0);
    world.add(Sphere::new(
        Point3::from([4.0, 1.0, 0.0]),
        1.0,
        Box::new(material_3),
    ));

    world
}

fn main() {
    const aspect_ratio: f64 = 16.0 / 9.0;
    const image_width: u32 = 300;
    const image_height: u32 = ((image_width as f64) / aspect_ratio) as u32;
    const samples_per_pixel: usize = 20;
    const max_depth: usize = 50;

    println!("P3\n{} {}\n255\n", image_width, image_height);

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
        aspect_ratio,
        aperture,
        dist_to_focus,
    );

    for (j, i) in iproduct!((0..image_height).rev(), (0..image_width)) {
        if i > 0 && image_width % i == 0 {
            eprint!("\rScanlines remaining: {}", j);
        }
        let pixel_color = (1..=samples_per_pixel)
            .map(|_| {
                let u = (i as f64 + random_double!()) / (image_width - 1) as f64;
                let v = (j as f64 + random_double!()) / (image_height - 1) as f64;
                let r = cam.get_ray(u, v);
                ray_color(&r, &world, max_depth)
            })
            .fold(Color::from([0.0, 0.0, 0.0]), |sum, c| sum + c);
        write_color(pixel_color, samples_per_pixel);
    }

    eprintln!("\nDone.");
}
