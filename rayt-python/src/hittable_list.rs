use pyo3::prelude::*;

use crate::{
    hittable::{HitRecord, Hittable},
    ray::Ray,
    sphere::Sphere,
};

#[derive(Default)]
#[pyclass]
pub struct HittableList {
    objects: Vec<Sphere>,
}

#[pymethods]
impl HittableList {
    #[new]
    fn py_new() -> Self {
        Self { objects: vec![] }
    }

    pub fn add(&mut self, object: Sphere) {
        self.objects.push(object);
    }
}

impl Hittable for HittableList {
    fn hit(&self, r: &Ray, t_min: f64, t_max: f64) -> Option<HitRecord> {
        let mut rec: Option<HitRecord> = None;
        let mut closest_so_far = t_max;

        for object in self.objects.iter() {
            if let Some(temp_rec) = object.hit(r, t_min, closest_so_far) {
                closest_so_far = temp_rec.t;
                rec = Some(temp_rec);
            }
        }

        rec
    }
}
