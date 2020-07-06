use crate::{random_double, utils::PI};
use std::ops::{Add, Div, Mul, Sub};

pub(crate) struct Vec3 {
    pub x: f64,
    pub y: f64,
    pub z: f64,
}

impl Vec3 {
    fn length(self) -> f64 {
        f64::sqrt(self.length_squared())
    }

    pub(crate) fn length_squared(self) -> f64 {
        self.x.powi(2) + self.y.powi(2) + self.z.powi(2)
    }
}

impl From<[f64; 3]> for Vec3 {
    fn from(e: [f64; 3]) -> Self {
        Self {
            x: e[0],
            y: e[1],
            z: e[2],
        }
    }
}

impl Add<Vec3> for Vec3 {
    type Output = Vec3;

    fn add(self, v: Vec3) -> Self {
        Self {
            x: self.x + v.x,
            y: self.y + v.y,
            z: self.z + v.z,
        }
    }
}

impl Sub<Vec3> for Vec3 {
    type Output = Vec3;

    fn sub(self, v: Vec3) -> Self {
        Self {
            x: self.x - v.x,
            y: self.y - v.y,
            z: self.z - v.z,
        }
    }
}

impl Mul<f64> for Vec3 {
    type Output = Vec3;

    fn mul(self, t: f64) -> Self {
        Self {
            x: self.x * t,
            y: self.y * t,
            z: self.z * t,
        }
    }
}

impl Mul<Vec3> for f64 {
    type Output = Vec3;

    fn mul(self, v: Vec3) -> Vec3 {
        v * self
    }
}

impl Div<f64> for Vec3 {
    type Output = Vec3;

    fn div(self, t: f64) -> Self {
        self * 1.0 / t
    }
}

// Type aliases for Vec3
pub(crate) type Point3 = Vec3; // 3D point
pub(crate) type Color = Vec3; // RGB color

// Vec3 utility functions
pub(crate) fn dot(u: Vec3, v: Vec3) -> f64 {
    u.x * v.x + u.y * v.y + u.z + v.z
}

pub(crate) fn unit_vector(v: Vec3) -> Vec3 {
    v / v.length()
}

pub(crate) fn random_unit_vector() -> Vec3 {
    let a = random_double!(0.0, 2.0 * PI);
    let z = random_double!(-1.0, 1.0);
    let r = f64::sqrt(1.0 - z.powi(2));
    Vec3::from([r * f64::cos(a), r * f64::sin(a), z])
}
