use rayt::vec3::{Color, Point3, Vec3};

#[test]
fn test_unary_minus_operator() {
    let vec3_pos = Vec3::from([0.5, 1.0, 2.5]);
    let vec3_neg = Vec3::from([-0.5, -1.0, -2.5]);
    assert_eq!(vec3_neg, -vec3_pos);
    assert_eq!(vec3_pos, -vec3_neg);

    let vec3_mix = Vec3::from([0.0, 2.3, -4.1]);
    assert_eq!(Vec3::from([0.0, -2.3, 4.1]), -vec3_mix);
}

#[test]
fn test_vec3_derived_types() {
    let vec3 = Vec3::from([1.0, 1.5, 2.0]);
    assert_eq!("Vec3 (1.0, 1.5, 2.0)", format!("{:?}", vec3));

    let point3 = Point3::from([1.0, 0.5, 0.0]);
    assert_eq!("Vec3 (1.0, 0.5, 0.0)", format!("{:?}", point3));

    let color = Color::from([255.0, 255.0, 255.0]);
    assert_eq!("Vec3 (255.0, 255.0, 255.0)", format!("{:?}", color));
}

#[test]
fn test_addition() {
    let vec3_1 = Vec3::from([-1.5, 0.5, -3.5]);
    let vec3_2 = Vec3::from([1.5, 0.5, 1.0]);
    assert_eq!(Vec3::from([0.0, 1.0, -2.5]), vec3_1 + vec3_2);
    assert_eq!(Vec3::from([0.0, 1.0, -2.5]), vec3_2 + vec3_1);
}

#[test]
fn test_subtraction() {
    let vec3_1 = Vec3::from([0.0, 1.0, -2.5]);
    let vec3_2 = Vec3::from([1.5, 0.5, 1.0]);
    assert_eq!(Vec3::from([-1.5, 0.5, -3.5]), vec3_1 - vec3_2);
    assert_eq!(Vec3::from([1.5, -0.5, 3.5]), vec3_2 - vec3_1);
}

#[test]
fn test_multiplication() {
    let vec3_1 = Vec3::from([0.0, 1.0, -2.5]);
    let vec3_2 = Vec3::from([1.5, 0.5, 1.0]);
    let double_1 = 2.0;
    assert_eq!(Vec3::from([0.0, 0.5, -2.5]), vec3_1 * vec3_2);
    assert_eq!(Vec3::from([0.0, 0.5, -2.5]), vec3_2 * vec3_1);
    assert_eq!(Vec3::from([3.0, 1.0, 2.0]), double_1 * vec3_2);
}

#[test]
fn test_true_division() {
    let vec3_1 = Vec3::from([1.0, 2.0, 3.0]);
    let vec3_2 = Vec3::from([0.5, -4.0, -1.2]);
    let double_1 = 2.0;
    assert_eq!(Vec3::from([2.0, -0.5, -2.5]), vec3_1 / vec3_2);
    assert_eq!(Vec3::from([0.25, -2.0, -0.6]), vec3_2 / double_1);
}

#[test]
fn test_vec3_length() {
    let vec3_1 = Vec3::from([1.0, 2.0, 3.0]);
    assert_eq!(14.0, vec3_1.length_squared());
    assert_eq!(3.7416573867739413, vec3_1.length());
}

#[test]
fn test_default_color() {
    assert_eq!(Color::from([0.0, 0.0, 0.0]), Color::default());
}
