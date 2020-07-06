use crate::{
    ray::Ray,
    vec3::{Point3, Vec3},
};

pub struct HitRecord {
    pub p: Point3,
    pub normal: Vec3,
    material: Material,
    t: f64,
    front_face: bool,
}

trait HitTable {
    fn hit(r: Ray, t_min: f64, t_max: f64, rec: HitRecord);
}
