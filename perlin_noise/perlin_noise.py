"""
Implementation of Perlin noise
"""
import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        return

def interp(u, v, w, deg=1) -> float:
    """
    Linearly interpolate between endpoints [u, v]
    :param u: (float) Lower bound for linear interpolation
    :param v: (float) Upper bound for linear interpolation
    :param w: (float) Weight. Should be in range [0, 1]
    :param deg: (int) Degree of polynomial to linearly interpolate
    :return: (float) Linear interpolation on interval [u, v]
    """
    if 0 > w:
        return u
    if 1 < w:
        return v
    if deg == 1:
        return u + (v - u) * w
    elif deg == 3:
        return (v - u) * (3 - 2 * w) * w**2 + u
    else:
        return (v - u) * ((w * (6 * w - 15) + 10) * w**3) + u


if __name__ == "__main__":
    p = Point(2, 5)




