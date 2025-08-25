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
fn rayt_python(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<camera::Camera>()?;
    m.add_class::<hittable_list::HittableList>()?;
    m.add_class::<material::Dielectric>()?;
    m.add_class::<material::Lambertian>()?;
    m.add_class::<material::Metal>()?;
    m.add_class::<ray::Ray>()?;
    m.add_class::<vec3::Vec3>()?;
    m.add_function(wrap_pyfunction!(color::get_color, m)?)?;
    m.add_function(wrap_pyfunction!(color::ray_color, m)?)?;
    m.add_function(wrap_pyfunction!(utils::random_double, m)?)?;
    m.add_function(wrap_pyfunction!(vec3::unit_vector, m)?)?;
    Ok(())
}
