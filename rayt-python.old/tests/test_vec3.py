from rayt_python.vec3_types import Color, Point3, Vec3


def test_unary_minus_operator():
    vec3_pos = Vec3(0.5, 1.0, 2.5)
    assert -vec3_pos == Vec3(-0.5, -1.0, -2.5)

    vec3_neg = Vec3(-0.5, -2.5, -1.0)
    assert -vec3_neg == Vec3(0.5, 2.5, 1.0)

    vec3_mix = Vec3(0.0, 2.3, -4.1)
    assert -vec3_mix == Vec3(0.0, -2.3, 4.1)


def test_vec3_derived_types():
    vec3 = Vec3(1.0, 1.5, 2.0)
    assert str(vec3) == "Vec3(1.0, 1.5, 2.0)"

    point3 = Point3(1.0, 0.5, 0.0)
    assert str(point3) == "Point3(1.0, 0.5, 0.0)"

    color = Color(255.0, 255.0, 255.0)
    assert str(color) == "Color(255.0, 255.0, 255.0)"


def test_addition():
    vec3_1 = Vec3(-1.5, 0.5, -3.5)
    vec3_2 = Vec3(1.5, 0.5, 1.0)
    assert vec3_1 + vec3_2 == Vec3(0.0, 1.0, -2.5)
    assert vec3_2 + vec3_1 == Vec3(0.0, 1.0, -2.5)


def test_subtraction():
    vec3_1 = Vec3(0.0, 1.0, -2.5)
    vec3_2 = Vec3(1.5, 0.5, 1.0)
    assert vec3_1 - vec3_2 == Vec3(-1.5, 0.5, -3.5)
    assert vec3_2 - vec3_1 == Vec3(1.5, -0.5, 3.5)


def test_multiplication():
    vec3_1 = Vec3(0.0, 1.0, -2.5)
    vec3_2 = Vec3(1.5, 0.5, 1.0)
    double_1 = 2.0
    assert vec3_1 * vec3_2 == Vec3(0.0, 0.5, -2.5)
    assert vec3_2 * vec3_1 == Vec3(0.0, 0.5, -2.5)
    assert vec3_1 * double_1 == Vec3(0.0, 2.0, -5.0)
    assert double_1 * vec3_2 == Vec3(3.0, 1.0, 2.0)


def test_true_division():
    vec3_1 = Vec3(1.0, 2.0, 3.0)
    vec3_2 = Vec3(0.5, -4.0, -1.2)
    double_1 = 2.0
    assert vec3_1 / vec3_2 == Vec3(2.0, -0.5, -2.5)
    assert vec3_2 / double_1 == Vec3(0.25, -2.0, -0.6)


def test_vec3_length():
    vec3_1 = Vec3(1.0, 2.0, 3.0)
    assert vec3_1.length_squared == 14.0
    assert vec3_1.length == 3.7416573867739413
