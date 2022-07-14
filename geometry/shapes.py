"""
Shapes!
"""

import re
from numpy import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class Particle:
    def __init__(self, x: float, y:float, r: float, name: str=None) -> None:
        """Circle of radius r centered at pt"""
        self.x = x
        self.y = y
        self.r = self.w = self.h = r
        self.name = name
        return 

    def __repr__(self) -> str:
        return f"Particle(({self.x}, {self.y}), {self.r})"

    def intersects_region(self, particle: "Particle") -> bool:
        """Test if this particle intersects with another given particle"""
        return (np.sqrt((self.x - particle.x)**2 + (self.y - particle.y)**2) <= self.r + particle.r)

    def contains_point(self, particle: "Particle") -> bool:
        """
        Test if bounding region contains Point
        point (Particle): Point being tested
        Returns a bool. True if point is within region, False otherwise
        """
        return (np.sqrt((self.x - particle.x)**2 + (self.y - particle.y)**2) <= self.r + particle.r)

    def draw_outline(self, ax, c: str="w", ec: str=None) -> None:
        """Draw outline of particle for plotting"""
        ax.add_patch(mpatches.Circle((self.x, self.y), self.r/50, color=c, ec=ec))
        return

class Rectangle:
    def __init__(self, x: float, y: float, w: float, h: float) -> None:
        """
        Rectangle. Used for defining bounding region of QuadTree
        x (float): x coordinate of center of rectangle
        y (float): y coordinate of center of rectangle
        w (float): half-width of rectangle
        h (float): half-height of rectangle
        """
        self.x = x
        self.y = y
        # (x,y) define the center of the rectangle in Cartesian coordinates
        self.w = w
        self.h = h
        return

    def contains_point(self, pt: Particle) -> bool:
        """
        Test if bounding region contains Point pt
        point (Particle): Point being tested
        Returns a bool. True if point is within region, False otherwise
        """
        return self.x - self.w < pt.x < self.x + self.w and self.y - self.h < pt.y < self.y + self.h

    def intersects_region(self, region: Particle or "Rectangle") -> bool:
        """
        Test if the rectangle intersects a given region
        :param region: (Rectangle) Region to test
        :return: Bool
        """
        return not (
                region.x - region.w > self.x + self.w or
                region.x + region.w < self.x - self.w or
                region.y - region.h > self.y + self.h or
                region.y + region.h < self.y - self.h
            )

    def draw_outline(self, ax: plt.axis, c: str="#0CFF00", lw: int=1) -> None:
        """
        Draw edges of QuadTree for visualization
        ax (plt.subplots()): axis to draw onto
        """
        # Rectangle will act as edge of QuadTree
        edge = mpatches.Rectangle(
            (self.x - self.w, self.y - self.h), self.w*2, self.h*2, ec=c, lw=lw, fill=False
        )
        ax.add_patch(edge)
        return

if __name__ == "__main__":
    ...
    
    

