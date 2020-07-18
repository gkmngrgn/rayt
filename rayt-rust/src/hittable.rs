use crate::{
    material::Material,
    ray::Ray,
    vec3::{dot, Point3, Vec3},
};

#[derive(Copy, Clone)]
pub(crate) struct HitRecord {
    pub(crate) p: Point3,
    pub(crate) normal: Vec3,
    pub(crate) material: Box<dyn Material>,
    pub(crate) t: f64,
    pub(crate) front_face: bool,
}

impl HitRecord {
    pub(crate) fn new(p: &Point3, t: f64, material: Box<dyn Material>) -> Self {
        Self {
            p: p.clone(),
            normal: Vec3::default(),
            material,
            t,
            front_face: false,
        }
    }

    pub(crate) fn set_face_normal(mut self, r: &Ray, outward_normal: &Vec3) {
        self.front_face = dot(&r.direction, outward_normal) < 0.0;
        self.normal = if self.front_face {
            *outward_normal
        } else {
            -*outward_normal
        };
    }
}

pub(crate) trait Hittable {
    fn hit(&self, r: &Ray, t_min: f64, t_max: f64) -> Option<HitRecord>;
}
