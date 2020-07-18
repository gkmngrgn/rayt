use crate::{
    hittable::{HitRecord, Hittable},
    material::Material,
    ray::Ray,
    vec3::{dot, Point3},
};

pub(crate) struct Sphere {
    center: Point3,
    radius: f64,
    material: Box<dyn Material>,
}

impl Sphere {
    pub(crate) fn new(center: Point3, radius: f64, material: Box<dyn Material>) -> Self {
        Self {
            center,
            radius,
            material,
        }
    }

    fn create_rec(self, r: &Ray, t: f64) -> HitRecord {
        let p = r.at(t);
        let mut rec = HitRecord::new(&p, t, self.material);
        rec.set_face_normal(r, &((p - self.center) / self.radius));
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
            let temp = (-half_b - root) / a;
            if temp < t_max && temp > t_min {
                return Some(self.create_rec(r, temp));
            }

            temp = (-half_b + root) / a;
            if temp > t_min && temp < t_max {
                return Some(self.create_rec(r, temp));
            }
        }

        None
    }
}
