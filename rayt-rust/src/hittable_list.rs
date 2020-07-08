use crate::hittable::{HitRecord, Hittable};
use crate::ray::Ray;
use crate::sphere::Sphere;

pub(crate) struct HittableList {
    objects: Vec<Sphere>,
}

impl HittableList {
    pub(crate) fn add(self, object: Sphere) {
        self.objects.push(object);
    }
}

impl Hittable for HittableList {
    fn hit(&self, r: &Ray, t_min: f64, t_max: f64, rec: &mut HitRecord) -> bool {
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
