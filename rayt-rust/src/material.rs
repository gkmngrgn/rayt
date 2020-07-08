use crate::hittable::HitRecord;
use crate::random_double;
use crate::ray::Ray;
use crate::vec3::{
    dot, random_in_unit_sphere, random_unit_vector, reflect, refract, unit_vector, Color,
};

pub(crate) enum Material {
    Lambertian(Lambertian),
    Metal(Metal),
    Dielectric(Dielectric),
}

impl Material {
    pub(crate) fn new_lambertian(albedo: Color) -> Self {
        Material::Lambertian(Lambertian::new(albedo))
    }

    pub(crate) fn new_metal(albedo: Color, fuzz: f64) -> Self {
        Material::Metal(Metal::new(albedo, fuzz))
    }

    pub(crate) fn new_dielectric(ref_idx: f64) -> Self {
        Material::Dielectric(Dielectric::new(ref_idx))
    }

    pub(crate) fn scatter(
        self,
        r_in: &Ray,
        rec: HitRecord,
        attenuation: Color,
        scattered: Ray,
    ) -> bool {
        match self {
            Material::Lambertian(m) => m.scatter(r_in, rec, attenuation, scattered),
            Material::Metal(m) => m.scatter(r_in, rec, attenuation, scattered),
            Material::Dielectric(m) => m.scatter(r_in, rec, attenuation, scattered),
        }
    }
}

impl Default for Material {
    fn default() -> Self {
        Material::Lambertian(Lambertian::new(Color::default()))
    }
}

struct Lambertian {
    albedo: Color,
}

impl Lambertian {
    fn new(albedo: Color) -> Self {
        Self { albedo }
    }

    fn scatter(self, r_in: &Ray, rec: HitRecord, attenuation: Color, scattered: Ray) -> bool {
        let scatter_direction = rec.normal + random_unit_vector();
        scattered = Ray::new(rec.p, scatter_direction);
        attenuation = self.albedo;
        true
    }
}

struct Metal {
    albedo: Color,
    fuzz: f64,
}

impl Metal {
    fn new(albedo: Color, fuzz: f64) -> Self {
        Self {
            albedo,
            fuzz: if fuzz < 1.0 { fuzz } else { 1.0 },
        }
    }

    fn scatter(self, r_in: &Ray, rec: HitRecord, attenuation: Color, scattered: Ray) -> bool {
        let reflected = reflect(unit_vector(r_in.direction), rec.normal);
        scattered = Ray::new(rec.p, reflected + self.fuzz * random_in_unit_sphere());
        attenuation = self.albedo;
        dot(&scattered.direction, &rec.normal) > 0.0
    }
}

struct Dielectric {
    ref_idx: f64,
}

impl Dielectric {
    fn new(ref_idx: f64) -> Self {
        Self { ref_idx }
    }

    fn scatter(self, r_in: &Ray, rec: HitRecord, attenuation: Color, scattered: Ray) -> bool {
        attenuation = Color::from([1.0, 1.0, 1.0]);
        let etai_over_etat = if rec.front_face {
            1.0 / self.ref_idx
        } else {
            self.ref_idx
        };

        let unit_direction = unit_vector(r_in.direction);
        let cos_theta = f64::min(dot(&-unit_direction, &rec.normal), 1.0);
        let sin_theta = f64::sqrt(1.0 - cos_theta.powi(2));

        if etai_over_etat * sin_theta > 1.0 {
            let reflected = reflect(unit_direction, rec.normal);
            scattered = Ray::new(rec.p, reflected);
            return true;
        }

        let reflect_prob = schlick(cos_theta, etai_over_etat);
        if random_double!() < reflect_prob {
            let reflected = reflect(unit_direction, rec.normal);
            scattered = Ray::new(rec.p, reflected);
            return true;
        }

        let refracted = refract(unit_direction, rec.normal, etai_over_etat);
        scattered = Ray::new(rec.p, refracted);
        true
    }
}

fn schlick(cosine: f64, ref_idx: f64) -> f64 {
    let r0 = ((1.0 - ref_idx) / (1.0 + ref_idx)).powi(2);
    r0 + (1.0 - r0) * (1.0 - cosine).powi(5)
}
