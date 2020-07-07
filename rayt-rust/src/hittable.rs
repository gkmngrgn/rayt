use crate::material::Material;
use crate::ray::Ray;
use crate::vec3::{dot, Point3, Vec3};

pub(crate) struct HitRecord {
    pub(crate) p: Point3,
    pub(crate) normal: Vec3,
    pub(crate) material: Material,
    pub(crate) t: f64,
    pub(crate) front_face: bool,
}

impl HitRecord {
    pub(crate) fn set_face_normal(self, r: Ray, outward_normal: Vec3) {
        self.front_face = dot(r.direction, outward_normal) < 0.0;
        self.normal = if self.front_face {
            outward_normal
        } else {
            -outward_normal
        };
    }
}

trait Hittable {
    fn hit(self, r: Ray, t_min: f64, t_max: f64, rec: HitRecord) -> bool;
}

pub(crate) struct Sphere {
    center: Point3,
    radius: f64,
    material: Material,
}

impl Sphere {
    pub(crate) fn new(center: Point3, radius: f64, material: Material) -> Self {
        Self {
            center,
            radius,
            material,
        }
    }
}

impl Hittable for Sphere {
    fn hit(self, r: Ray, t_min: f64, t_max: f64, rec: HitRecord) -> bool {
        let oc = r.origin - self.center;
        let a = r.direction.length_squared();
        let half_b = dot(oc, r.direction);
        let c = oc.length_squared() - self.radius.powi(2);
        let discriminant = half_b.powi(2) - a * c;

        if discriminant > 0.0 {
            let root = f64::sqrt(discriminant);
            let temp = (-half_b - root) / a;
            if temp < t_max && temp > t_min {
                rec.t = temp;
                rec.p = r.at(rec.t);
                rec.normal = (rec.p - self.center) / self.radius;

                let outward_normal = (rec.p - self.center) / self.radius;
                rec.set_face_normal(r, outward_normal);
                rec.material = self.material;
                return true;
            }

            temp = (-half_b + root) / a;
            if temp < t_max && temp > t_min {
                rec.t = temp;
                rec.p = r.at(rec.t);
                rec.normal = (rec.p - self.center) / self.radius;

                let outward_normal = (rec.p - self.center) / self.radius;
                rec.set_face_normal(r, outward_normal);
                rec.material = self.material;
                return true;
            }
        }

        false
    }
}

pub(crate) struct World {
    objects: Vec<Sphere>,
}

impl World {
    pub(crate) fn hit(self, r: Ray, t_min: f64, t_max: f64, rec: HitRecord) -> bool {
        self.hit(r, t_min, t_max, rec)
    }

    pub(crate) fn add(self, object: Sphere) {
        self.objects.push(object);
    }
}

impl Hittable for World {
    fn hit(self, r: Ray, t_min: f64, t_max: f64, rec: HitRecord) -> bool {
        let temp_rec;
        let mut hit_anything = false;
        let mut closest_so_far = t_max;

        for object in self.objects {
            if object.hit(r, t_min, closest_so_far, temp_rec) {
                hit_anything = true;
                closest_so_far = temp_rec.t;
                rec = temp_rec;
            }
        }

        hit_anything
    }
}
