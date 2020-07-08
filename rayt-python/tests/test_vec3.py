from rayt_python.vec3 import Vec3


def test_addition():
    vec3_1 = Vec3(-1.5, 0.5, -3.5)
    vec3_2 = Vec3(1.5, 0.5, 1.0)
    assert vec3_1 + vec3_2 == vec3_2 + vec3_1
    assert vec3_1 + vec3_2 == Vec3(0.0, 1.0, -2.5)


def test_subtraction():
    vec3_1 = Vec3(0.0, 1.0, -2.5)
    vec3_2 = Vec3(1.5, 0.5, 1.0)
    assert vec3_1 - vec3_2 == Vec3(-1.5, 0.5, -3.5)
    assert vec3_2 - vec3_1 == Vec3(1.5, -0.5, 3.5)
