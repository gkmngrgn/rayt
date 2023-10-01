use std::fmt;
use std::ops::{Add, Div, Mul, MulAssign, Neg, Sub};

use pyo3::{pyclass, pyfunction, pymethods};

use crate::{
    random_double,
    utils::{random_double, PI},
};

#[pyclass]
#[derive(PartialEq, Clone, Copy, Default)]
pub struct Vec3 {
    pub x: f64,
    pub y: f64,
    pub z: f64,
}

#[pymethods]
impl Vec3 {
    #[staticmethod]
    pub fn random(min: Option<f64>, max: Option<f64>) -> Self {
        Self {
            x: random_double(min, max),
            y: random_double(min, max),
            z: random_double(min, max),
        }
    }

    pub fn length(&self) -> f64 {
        f64::sqrt(self.length_squared())
    }

    pub fn length_squared(&self) -> f64 {
        self.x.powi(2) + self.y.powi(2) + self.z.powi(2)
    }
}

impl fmt::Debug for Vec3 {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Vec3 ({:?}, {:?}, {:?})", self.x, self.y, self.z)
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

    fn add(self, rhs: Vec3) -> Self::Output {
        Self::Output {
            x: self.x + rhs.x,
            y: self.y + rhs.y,
            z: self.z + rhs.z,
        }
    }
}

impl Sub<Vec3> for Vec3 {
    type Output = Vec3;

    fn sub(self, rhs: Vec3) -> Self::Output {
        Self::Output {
            x: self.x - rhs.x,
            y: self.y - rhs.y,
            z: self.z - rhs.z,
        }
    }
}

impl Mul<Vec3> for Vec3 {
    type Output = Vec3;

    fn mul(self, rhs: Vec3) -> Self::Output {
        Self::Output {
            x: self.x * rhs.x,
            y: self.y * rhs.y,
            z: self.z * rhs.z,
        }
    }
}

impl Mul<f64> for Vec3 {
    type Output = Vec3;

    fn mul(self, rhs: f64) -> Self::Output {
        Self::Output {
            x: self.x * rhs,
            y: self.y * rhs,
            z: self.z * rhs,
        }
    }
}

impl Mul<Vec3> for f64 {
    type Output = Vec3;

    fn mul(self, rhs: Vec3) -> Self::Output {
        rhs * self
    }
}

impl MulAssign<Vec3> for Vec3 {
    fn mul_assign(&mut self, rhs: Vec3) {
        *self = Self {
            x: self.x * rhs.x,
            y: self.y * rhs.y,
            z: self.z * rhs.z,
        }
    }
}

impl Div<Vec3> for Vec3 {
    type Output = Vec3;

    fn div(self, rhs: Vec3) -> Self::Output {
        Self::Output {
            x: self.x / rhs.x,
            y: self.y / rhs.y,
            z: self.z / rhs.z,
        }
    }
}

impl Div<f64> for Vec3 {
    type Output = Vec3;

    fn div(self, rhs: f64) -> Self::Output {
        self * (1.0 / rhs)
    }
}

impl Neg for Vec3 {
    type Output = Vec3;

    fn neg(self) -> Self::Output {
        Self::Output {
            x: -self.x,
            y: -self.y,
            z: -self.z,
        }
    }
}

// Vec3 utility functions
pub fn dot(u: &Vec3, v: &Vec3) -> f64 {
    u.x * v.x + u.y * v.y + u.z * v.z
}

pub fn cross(u: Vec3, v: Vec3) -> Vec3 {
    Vec3::from([
        u.y * v.z - u.z * v.y,
        u.z * v.x - u.x * v.z,
        u.x * v.y - u.y * v.x,
    ])
}

#[pyfunction]
pub fn unit_vector(v: Vec3) -> Vec3 {
    v / v.length()
}

pub fn random_in_unit_sphere() -> Vec3 {
    loop {
        let p = Vec3::random(Some(-1.0), Some(1.0));
        if p.length_squared() >= 1.0 {
            continue;
        }
        return p;
    }
}

pub fn random_unit_vector() -> Vec3 {
    let a = random_double!(0.0, 2.0 * PI);
    let z = random_double!(-1.0, 1.0);
    let r = f64::sqrt(1.0 - z.powi(2));
    Vec3::from([r * f64::cos(a), r * f64::sin(a), z])
}

pub fn random_in_unit_disk() -> Vec3 {
    loop {
        let p = Vec3::from([random_double!(-1.0, 1.0), random_double!(-1.0, 1.0), 0.0]);
        if p.length_squared() >= 1.0 {
            continue;
        }
        return p;
    }
}

pub fn reflect(v: Vec3, n: Vec3) -> Vec3 {
    v - 2.0 * dot(&v, &n) * n
}

pub fn refract(uv: Vec3, n: Vec3, etai_over_etat: f64) -> Vec3 {
    let cos_theta = dot(&-uv, &n);
    let r_out_parallel = etai_over_etat * (uv + cos_theta * n);
    let r_out_perp = -f64::sqrt(1.0 - r_out_parallel.length_squared()) * n;
    r_out_parallel + r_out_perp
}
