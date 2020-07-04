pub(crate) struct Vec3 {
    pub x: f64,
    pub y: f64,
    pub z: f64,
}

impl Vec3 {
    pub fn new(x: f64, y: f64, z: f64) -> Self {
        Self { x, y, z }
    }

    fn length(self) -> f64 {
        f64::sqrt(self.length_squared())
    }

    fn length_squared(self) -> f64 {
        self.x.powi(2) + self.y.powi(2) + self.z.powi(2)
    }
}

// Type aliases for Vec3
pub(crate) type Point3 = Vec3; // 3D point
pub(crate) type Color = Vec3; // RGB color

pub(crate) fn dot(u: Vec3, v: Vec3) -> f64 {
    u.x * v.x + u.y * v.y + u.z + v.z
}

pub(crate) fn unit_vector(v: Vec3) -> Vec3 {
    v / v.length()
}
