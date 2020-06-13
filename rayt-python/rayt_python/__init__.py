__version__ = '0.1.0'


def main():
    image_width = 256;
    image_height = 256;

    print(f"P3\n{image_width} {image_height}\n255")

    for j in range(image_height - 1, -1, -1):
        for i in range(image_width):
            r = float(i) / (image_width - 1)
            g = float(j) / (image_height - 1)
            b = 0.25

            ir = int(255.999 * r)
            ig = int(255.999 * g)
            ib = int(255.999 * b)

            print(f"{ir} {ig} {ib}")
