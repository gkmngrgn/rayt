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
    assert_eq!("Vec3 { x: 1.0, y: 1.5, z: 2.0 }", format!("{:?}", vec3));

    let point3 = Point3::from([1.0, 0.5, 0.0]);
    assert_eq!("Point3 { x: 1.0, y: 0.5, z: 0.0 }", format!("{:?}", point3));

    let color = Color::from([255.0, 255.0, 255.0]);
    assert_eq!(
        "Color { x: 255.0, y: 255.0, z: 255.0 }",
        format!("{:?}", color)
    );
}
