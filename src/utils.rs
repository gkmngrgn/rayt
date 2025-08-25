use pyo3::prelude::*;

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

#[pyfunction]
#[pyo3(signature = (min=0.0, max=1.0, /))]
pub fn random_double(min: f64, max: f64) -> f64 {
    random_double!(min, max)
}
