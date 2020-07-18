use crate::{utils::clamp, vec3::Color};

fn get_color_str(pixel_color: Color, samples_per_pixel: usize) -> String {
    let scale = 1.0 / samples_per_pixel as f64;
    let get_color = |c| (255.999 * clamp(f64::sqrt(scale * c), 0.0, 0.999)) as u32;
    let r = get_color(pixel_color.x);
    let g = get_color(pixel_color.y);
    let b = get_color(pixel_color.z);
    format!("{} {} {}", r, g, b)
}

pub fn write_color(pixel_color: Color, samples_per_pixel: usize) {
    println!("{}", get_color_str(pixel_color, samples_per_pixel));
}
