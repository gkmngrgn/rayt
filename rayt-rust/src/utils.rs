// Constants
const INFINITY: f64 = f64::INFINITY;
const PI: f64 = f64::PI;

// Macros
#[macro_export]
macro_rules! random_double {
    () => {
        rand::random::<f64>()
    };
    ($min:expr, $max:expr) => {
        $min + ($max - $min) * random_double!()
    };
}

// Utility functions
pub fn degrees_to_radians(degrees: f64) -> f64 {
    degrees * PI / 180_f64
}

pub fn clamp(x: f64, min: f64, max: f64) -> f64 {
    match x {
        n if n < min => min,
        n if n > max => max,
        _ => x,
    }
}
