use pyo3::prelude::*;

use crate::{
    hittable::Hittable,
    hittable_list::HittableList,
    material::Scatter,
    ray::Ray,
    utils::{clamp, INFINITY},
    vec3::{unit_vector, Color},
};

#[pyfunction]
pub fn get_color(pixel_color: Color, samples_per_pixel: usize) -> String {
    let scale = 1.0 / samples_per_pixel as f64;
    let color = |c| (255.999 * clamp(f64::sqrt(scale * c), 0.0, 0.999)) as u32;
    format!(
        "{} {} {}",
        color(pixel_color.x),
        color(pixel_color.y),
        color(pixel_color.z)
    )
}

#[pyfunction]
pub fn ray_color(mut r: Ray, world: &HittableList, depth: usize) -> Color {
    if depth == 0 {
        return Color::default();
    }

    let mut r_color = Color::from([1.0, 1.0, 1.0]);

    for _ in 0..depth {
        match world.hit(&r, 0.001, INFINITY) {
            Some(rec) => match rec.material.scatter(&r, rec) {
                Some((scattered, attenuation)) => {
                    r = scattered;
                    r_color *= attenuation;
                }
                None => return Color::default(),
            },
            None => {
                let unit_direction = unit_vector(r.direction);
                let t = 0.5 * (unit_direction.y + 1.0);
                r_color *=
                    (1.0 - t) * Color::from([1.0, 1.0, 1.0]) + t * Color::from([0.5, 0.7, 1.0]);
                break;
            }
        }
    }

    r_color
}
