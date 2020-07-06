use crate::hittable::HitRecord;
use crate::ray::Ray;
use crate::vec3::{random_unit_vector, Color};

trait Material {
    fn scatter(self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray);
}

struct Lambertian {
    albedo: Color,
}

impl Material for Lambertian {
    fn scatter(self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray) {
        let scatter_direction = rec.normal + random_unit_vector();
        scattered = Ray::new(rec.p, scatter_direction);
        attenuation = self.albedo;
        true
    }
}
