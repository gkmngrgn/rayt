use pyo3::prelude::*;

use crate::{
    hittable::{HitRecord, Hittable},
    material::Material,
    ray::Ray,
    sphere::Sphere,
    vec3::{Color, Point3},
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

    fn add_lambertian(&mut self, center: Point3, radius: f64, albedo: Color) {
        let material = Material::new_lambertian(albedo);
        let sphere = Sphere::new(center, radius, material);
        self.add(sphere);
    }

    fn add_metal(&mut self, center: Point3, radius: f64, albedo: Color, fuzz: f64) {
        let material = Material::new_metal(albedo, fuzz);
        let sphere = Sphere::new(center, radius, material);
        self.add(sphere);
    }

    fn add_dielectric(&mut self, center: Point3, radius: f64, ref_idx: f64) {
        let material = Material::new_dielectric(ref_idx);
        let sphere = Sphere::new(center, radius, material);
        self.add(sphere);
    }

    fn get_sphere_data(&self) -> Vec<Vec<f64>> {
        let mut data = vec![];

        for object in self.objects.iter() {
            data.push(vec![
                object.center.x,
                object.center.y,
                object.center.z,
                object.radius,
            ]);
        }

        data
    }

    fn get_material_data(&self) -> Vec<Vec<f64>> {
        let mut data = vec![];

        for object in self.objects.iter() {
            let material_data = match object.material {
                Material::Lambertian(m) => {
                    vec![0.0, m.albedo.x, m.albedo.y, m.albedo.z, 0.0]
                }
                Material::Metal(m) => {
                    vec![1.0, m.albedo.x, m.albedo.y, m.albedo.z, m.fuzz]
                }
                Material::Dielectric(m) => vec![2.0, m.ref_idx, 0.0, 0.0, 0.0],
            };
            data.push(material_data);
        }

        data
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
