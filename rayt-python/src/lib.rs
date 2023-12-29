use pyo3::prelude::*;

mod camera;
mod color;
mod hittable;
mod hittable_list;
mod material;
mod ray;
mod sphere;
mod utils;
mod vec3;

/// A Python module implemented in Rust.
#[pymodule]
fn rayt_python(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<camera::Camera>()?;
    m.add_class::<hittable_list::HittableList>()?;
    m.add_class::<ray::Ray>()?;
    m.add_class::<vec3::Color>()?;
    m.add_class::<vec3::Point3>()?;
    m.add_class::<vec3::Vec3>()?;
    m.add_function(wrap_pyfunction!(color::write_color, m)?)?;
    m.add_function(wrap_pyfunction!(utils::random_double, m)?)?;
    m.add_function(wrap_pyfunction!(vec3::unit_vector, m)?)?;
    Ok(())
}
