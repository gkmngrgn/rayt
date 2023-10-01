use pyo3::prelude::*;

mod camera;
mod color;
mod ray;
mod utils;
mod vec3;

/// `rayt-rust` python bindings
#[pymodule]
fn rayt_rust_py(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<ray::Ray>()?;
    m.add_class::<vec3::Vec3>()?;
    m.add_function(wrap_pyfunction!(color::write_color, m)?)?;
    m.add_function(wrap_pyfunction!(utils::random_double, m)?)?;
    m.add_function(wrap_pyfunction!(vec3::unit_vector, m)?)?;
    Ok(())
}
