use pyo3::prelude::*;

use crate::{
    hittable::{HitRecord, Hittable},
    material::Material,
    ray::Ray,
    vec3::{dot, Point3},
};

#[derive(Clone, Copy)]
#[pyclass]
pub struct Sphere {
    pub center: Point3,
    pub radius: f64,
    pub material: Material,
}

impl Sphere {
    pub fn new(center: Point3, radius: f64, material: Material) -> Self {
        Self {
            center,
            radius,
            material,
        }
    }

    fn create_rec(&self, r: &Ray, t: f64) -> HitRecord {
        let p = r.at(t);
        let outward_normal = (p - self.center) / self.radius;
        let mut rec = HitRecord::new(p, outward_normal, t, self.material);
        rec.set_face_normal(r, &outward_normal);
        rec
    }
}

impl Hittable for Sphere {
    fn hit(&self, r: &Ray, t_min: f64, t_max: f64) -> Option<HitRecord> {
        let oc = r.origin - self.center;
        let a = r.direction.length_squared();
        let half_b = dot(&oc, &r.direction);
        let c = oc.length_squared() - self.radius.powi(2);
        let discriminant = half_b.powi(2) - a * c;

        if discriminant > 0.0 {
            let root = f64::sqrt(discriminant);
            let mut temp = (-half_b - root) / a;
            if temp < t_max && temp > t_min {
                return Some(self.create_rec(r, temp));
            }

            temp = (-half_b + root) / a;
            if temp < t_max && temp > t_min {
                return Some(self.create_rec(r, temp));
            }
        }

        None
    }
}
