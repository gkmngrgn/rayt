use pyo3::prelude::*;

use crate::{utils::clamp, vec3::Color};

#[pyfunction]
pub fn write_color(pixel_color: Color, samples_per_pixel: usize) {
    let scale = 1.0 / samples_per_pixel as f64;
    let get_color = |c| (255.999 * clamp(f64::sqrt(scale * c), 0.0, 0.999)) as u32;
    let r = get_color(pixel_color.x);
    let g = get_color(pixel_color.y);
    let b = get_color(pixel_color.z);
    println!("{} {} {}", r, g, b)
}
