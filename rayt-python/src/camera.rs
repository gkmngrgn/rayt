use pyo3::prelude::*;

use crate::{
    ray::Ray,
    utils::degrees_to_radians,
    vec3::{cross, random_in_unit_disk, unit_vector, Point3, Vec3},
};

#[pyclass]
pub struct Camera {
    origin: Point3,
    lower_left_corner: Point3,
    horizontal: Vec3,
    vertical: Vec3,
    u: Vec3,
    v: Vec3,
    lens_radius: f64,
}

#[pymethods]
impl Camera {
    #[new]
    pub fn py_new(
        lookfrom: [f64; 3],
        lookat: [f64; 3],
        vup: [f64; 3],
        vfov: f64,
        aspect_ratio: f64,
        aperture: f64,
        focus_dist: f64,
    ) -> Self {
        let theta = degrees_to_radians(vfov);
        let h = f64::tan(theta / 2.0);
        let viewport_height = 2.0 * h;
        let viewport_width = aspect_ratio * viewport_height;

        let lookfrom_point3 = Point3::from(lookfrom);
        let lookat_point3 = Point3::from(lookat);
        let vup_point3 = Vec3::from(vup);

        let w = unit_vector(lookfrom_point3 - lookat_point3);
        let u = unit_vector(cross(vup_point3, w));
        let v = cross(w, u);

        let origin = lookfrom_point3;
        let horizontal = focus_dist * viewport_width * u;
        let vertical = focus_dist * viewport_height * v;
        let lower_left_corner = origin - horizontal / 2.0 - vertical / 2.0 - focus_dist * w;
        let lens_radius = aperture / 2.0;

        Self {
            origin,
            lower_left_corner,
            horizontal,
            vertical,
            u,
            v,
            lens_radius,
        }
    }

    pub fn get_ray(&self, s: f64, t: f64) -> Ray {
        let rd = self.lens_radius * random_in_unit_disk();
        let offset = self.u * rd.x + self.v * rd.y;
        Ray {
            origin: self.origin + offset,
            direction: self.lower_left_corner + s * self.horizontal + t * self.vertical
                - self.origin
                - offset,
        }
    }
}
