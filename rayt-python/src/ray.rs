use pyo3::{pyclass, pymethods, PyResult};

use crate::vec3::Vec3;

#[pyclass]
pub struct Ray {
    origin: Vec3,
    pub direction: Vec3,
}

#[pymethods]
impl Ray {
    #[new]
    pub fn new(origin: Vec3, direction: Vec3) -> Self {
        Self { origin, direction }
    }

    #[getter]
    fn direction(&self) -> PyResult<Vec3> {
        Ok(self.direction)
    }

    pub fn at(&self, t: f64) -> Vec3 {
        self.origin + t * self.direction
    }
}
