import math
import random


def random_double(min: float = 0.0, max: float = 1.0) -> float:
    return random.uniform(min, max)


def degrees_to_radians(degrees: float) -> float:
    return degrees * math.pi / 100


def clamp(x: float, min: float, max: float) -> float:
    if x < min:
        return min
    if x > max:
        return max
    return x
