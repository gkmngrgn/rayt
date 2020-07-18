use crate::{
    hittable::HitRecord,
    random_double,
    ray::Ray,
    vec3::{dot, random_in_unit_sphere, random_unit_vector, reflect, refract, unit_vector, Color},
};

pub(crate) trait Material {
    fn scatter(self, r_in: &Ray, rec: &HitRecord) -> Option<(Ray, Color)>;
}

pub(crate) struct Lambertian {
    albedo: Color,
}

impl Lambertian {
    pub(crate) fn new(albedo: Color) -> Self {
        Self { albedo }
    }
}

impl Material for Lambertian {
    fn scatter(self, r_in: &Ray, rec: &HitRecord) -> Option<(Ray, Color)> {
        let scatter_direction = rec.normal + random_unit_vector();
        let scattered = Ray::new(rec.p, scatter_direction);
        let attenuation = self.albedo;
        Some((scattered, attenuation))
    }
}

pub(crate) struct Metal {
    albedo: Color,
    fuzz: f64,
}

impl Metal {
    pub(crate) fn new(albedo: Color, fuzz: f64) -> Self {
        Self {
            albedo,
            fuzz: if fuzz < 1.0 { fuzz } else { 1.0 },
        }
    }
}

impl Material for Metal {
    fn scatter(self, r_in: &Ray, rec: &HitRecord) -> Option<(Ray, Color)> {
        let reflected = reflect(unit_vector(r_in.direction), rec.normal);
        let scattered = Ray::new(rec.p, reflected + self.fuzz * random_in_unit_sphere());
        let attenuation = self.albedo;
        if dot(&scattered.direction, &rec.normal) > 0.0 {
            Some((scattered, attenuation))
        } else {
            None
        }
    }
}

pub(crate) struct Dielectric {
    ref_idx: f64,
}

impl Dielectric {
    pub(crate) fn new(ref_idx: f64) -> Self {
        Self { ref_idx }
    }
}

impl Material for Dielectric {
    fn scatter(self, r_in: &Ray, rec: &HitRecord) -> Option<(Ray, Color)> {
        let attenuation = Color::from([1.0, 1.0, 1.0]);
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
            let scattered = Ray::new(rec.p, reflected);
            return Some((scattered, attenuation));
        }

        let reflect_prob = schlick(cos_theta, etai_over_etat);
        if random_double!() < reflect_prob {
            let reflected = reflect(unit_direction, rec.normal);
            let scattered = Ray::new(rec.p, reflected);
            return Some((scattered, attenuation));
        }

        let refracted = refract(unit_direction, rec.normal, etai_over_etat);
        let scattered = Ray::new(rec.p, refracted);
        Some((scattered, attenuation))
    }
}

fn schlick(cosine: f64, ref_idx: f64) -> f64 {
    let r0 = ((1.0 - ref_idx) / (1.0 + ref_idx)).powi(2);
    r0 + (1.0 - r0) * (1.0 - cosine).powi(5)
}
