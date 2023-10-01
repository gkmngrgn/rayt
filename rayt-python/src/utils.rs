use pyo3::pyfunction;

// Constants
pub const INFINITY: f64 = f64::INFINITY;
pub const PI: f64 = std::f64::consts::PI;

// Macros
#[macro_export]
macro_rules! random_double {
    () => {
        rand::random::<f64>()
    };
    ($min:expr, $max:expr) => {
        $min + ($max - $min) * random_double!()
    };
    ($min_max:expr) => {
        match $min_max {
            Some(min_max) => random_double!(min_max[0], min_max[1]),
            None => random_double!(),
        }
    };
}

// Utility functions
#[pyfunction]
pub fn random_double(min: Option<f64>, max: Option<f64>) -> f64 {
    let min = min.unwrap_or(0.0);
    let max = max.unwrap_or(1.0);
    min + (max - min) * rand::random::<f64>()
}

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
