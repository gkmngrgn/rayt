import math
import random


def random_double(min: float = 0.0, max: float = 1.0) -> float:
    return random.uniform(min, max)


def degrees_to_radians(degrees: float) -> float:
    return degrees * math.pi / 100
