"""
Implementation of QuadTree data structure
"""
from dis import dis
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from geometry.shapes import Particle, Rectangle


class QuadTree:
    def __init__(self, boundary: Rectangle, capacity: int=4) -> None:
        """
        QuadTree data structure
        boundary (Rectangle): Bounding region of the QuadTree
        capacity (int): Maximum capacity of QuadTree. Default is 4
        """
        self.boundary = boundary # boundary of region
        self.capacity = capacity # Max number of points allowed in region
        self.points = [] # Points within this region
        self.daughters = [] # Daughter nodes
        self.divided = False # Whether or not this QuadTree is divided already
        return

    def __repr__(self):
        """
        Get representation of QuadTree
        """
        return f"QuadTree spawned at ({self.boundary.x}, {self.boundary.y}) contains {len(self.points)} points"

    def _subdivide(self) -> None:
        """
        Subdivide the quad tree
        """
        # some local variables
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        # Define northeast region of QuadTree
        ne = Rectangle(x + w/2, y + h/2, w/2, h/2)
        self.northeast = QuadTree(ne, self.capacity)
        self.daughters.append(self.northeast)
        # Define northwest region of QuadTree
        nw = Rectangle(x - w/2, y + h/2, w/2, h/2)
        self.northwest = QuadTree(nw, self.capacity)
        self.daughters.append(self.northwest)
        # Define southeast region of QuadTree
        se = Rectangle(x + w/2, y - h/2, w/2, h/2)
        self.southeast = QuadTree(se, self.capacity)
        self.daughters.append(self.southeast)
        # Define southwest region of QuadTree
        sw = Rectangle(x - w/2, y - h/2, w/2, h/2)
        self.southwest = QuadTree(sw, self.capacity)
        self.daughters.append(self.southwest)
        # Set bool to true
        self.divided = True
        # Add daughter nodes to list
        return

    def quad_tree_display(self) -> dict:
        """
        Dictionary of all QuadTree nodes for display
        """
        QT = {}
        for qtree in self.daughters:
            if qtree.divided:
                #try:
                qtree.quad_tree_display()
                #except AttributeError:
                    #print(f"No more daughter nodes!")
            else:
                QT[f"{qtree}"] = qtree.points
                print(f"{qtree}")
                for p in qtree.points:
                    print(f"    Point at {(p.x, p.y)}")
        return QT

    def insert_point(self, point: Particle) -> None:
        """
        Insert point into the QuadTree
        If the QuadTree is already at maximum capacity, subdivide the QuadTree
        point (Particle): Point being inserted into QuadTree
        """
        # Check if point is within bounding region
        if not self.boundary.contains_point(point):
            return
        else:
            if len(self.points) < self.capacity:
                self.points.append(point)
            else:
                if not self.divided:
                    self._subdivide()
                # Insert points to daughter nodes
                self.northeast.insert_point(point)
                self.northwest.insert_point(point)
                self.southeast.insert_point(point)
                self.southwest.insert_point(point)
            return

    def draw_outline(self, ax: plt.axis, c: str="w") -> None:
        """
        Draw edges of QuadTree for visualization
        ax (plt.subplots()): axis to draw onto
        """
        # Rectangle will act as edge of QuadTree
        qt_edge = mpatches.Rectangle(
            (self.boundary.x - self.boundary.w, self.boundary.y - self.boundary.h),
            self.boundary.w*2,
            self.boundary.h*2,
            lw=0.2, fill=False, ec=c
        )
        ax.add_patch(qt_edge)

        # If the QuadTree has divided, draw the edges of the daughter nodes also
        if self.divided:
            self.northeast.draw_outline(ax)
            self.northwest.draw_outline(ax)
            self.southeast.draw_outline(ax)
            self.southwest.draw_outline(ax)
        return

    def query_region(self, region: Particle or Rectangle, found: list=[]) -> list:
        """
        Find points within a given region
        :param found: (array) List of points found within specified region
        :param region: (Rectangle) Region to query points
        :return:
        """
        # Determine if any points are found in region already
        if not found:
            found = []
        # Determine if region and QuadTree overlap
        if not self.boundary.intersects_region(region):
            return found
        else:
            # Iterate through all points within QuadTree and determine if they are also within region of intersection
            for p in self.points:
                if region.contains_point(p):
                    found.append(p)
            # If the region has subdivided, determine which points are within the regions spawned from this node
            if self.divided:
                self.northeast.query_region(region, found)
                self.northwest.query_region(region, found)
                self.southeast.query_region(region, found)
                self.southwest.query_region(region, found)
            return found


if __name__ == "__main__":
    # Define points in space and QuadTree
    a, b = range(20), range(20)
    rect = Rectangle(x=0, y=0, w=10, h=10)
    qt = QuadTree(boundary=rect, capacity=4)
    # Inserting points into the QuadTree
    for x, y in zip(a, b):
        qt.insert_point(Particle(x, y))


    






