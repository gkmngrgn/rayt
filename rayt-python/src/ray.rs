use pyo3::prelude::*;

use crate::vec3::{Point3, Vec3};

#[pyclass]
pub struct Ray {
    pub origin: Point3,
    pub direction: Vec3,
}

#[pymethods]
impl Ray {
    #[new]
    pub fn py_new(origin: Point3, direction: Vec3) -> Self {
        Self { origin, direction }
    }

    pub fn at(&self, t: f64) -> Point3 {
        self.origin + t * self.direction
    }
}
