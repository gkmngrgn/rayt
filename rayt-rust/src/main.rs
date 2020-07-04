#[macro_use]
extern crate itertools;

fn hit_sphere() {
    // TODO:
}

fn ray_color() {
    // TODO:
}

fn random_scene() {
    // TODO:
}

fn main() {
    const aspect_ratio: f64 = 16.0 / 9.0;
    const image_width: u32 = 300;
    const image_height: u32 = ((image_width as f64) / aspect_ratio) as u32;
    const samples_per_pixel: usize = 20;
    const max_depth: usize = 50;

    println!("P3\n{} {}\n255\n", image_width, image_height);

    let world = random_scene();
    let lookfrom = Point3::new(13, 2, 3);
    let lookat = Point3::new(0, 0, 0);
    let vup = Vec3::new(0, 1, 0);
    let dist_to_focus = 10.0;
    let aperture = 0.1;

    let cam = Camera::new(
        lookfrom,
        lookat,
        vup,
        20,
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
                let u = (i + random_double()) / (image_width - 1);
                let v = (j + random_double()) / (image_height - 1);
                let r = cam.get_ray(u, v);
                ray_color(r, world, max_depth)
            })
            .fold(Color::new(0.0, 0.0, 0.0), |sum, c| sum + c);
        write_color(pixel_color, samples_per_pixel);
    }

    eprintln!("\nDone.");
}
