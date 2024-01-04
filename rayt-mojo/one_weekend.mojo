# vec3

@value
struct Vec3:
    var x: Float64
    var y: Float64
    var z: Float64


alias Point3 = Vec3
alias Color = Vec3


# ray

@value
struct Ray:
    var origin: Point3
    var direction: Vec3

    fn at(self, t: Float64) -> Point3:
        return self.origin + t * self.direction

# material

trait Material:
    fn scatter(self, r_in: Ray, rec: HitRecord):
        ...


@value
struct Lambertian(Material): None


@value
struct Metal(Material): None


@value
struct Dielectric(Material): None


# sphere

@value
struct Sphere:
    var center: Point3
    var radius: Float64
    var material: Material


# hittable

@value
struct HitRecord:
    var p: Point3
    var normal: Vec3
    var material: Material
    var t: Float64
    var front_face: Bool


@value
struct HittableList:
    var objects: DynamicVector[Int]

    fn __init__(inout self, objects: DynamicVector[Int] = DynamicVector[Int]()):
        self.objects = objects


# main
fn random_scene() -> HittableList:
    world = HittableList()
    # TODO: not done yet.
    return world


fn one_weekend(aspect_ratio: Float64, image_width: Int, samples_per_pixel: Int, max_depth: Int) -> None:
    let image_height: Int = int(image_width / aspect_ratio)
    let world = random_scene()

    print("P3")
    print(f"{image_width} {image_height}")
    print("255")


# run
fn main():
    let hittable_list = HittableList()
    one_weekend(
        aspect_ratio=16.0 / 9.0,
        image_width=300,
        samples_per_pixel=20,
        max_depth=50,
    )
