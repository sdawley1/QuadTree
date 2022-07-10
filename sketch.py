"""
QuadTrees!
"""

from numpy.random import default_rng
import matplotlib.pyplot as plt
from qtree.quad_tree import Point, QuadTree, Rectangle

def draw():
    """
    Draw all elements of matplotlib figure
    :return:
    """
    # Establish QuadTree
    rect = Rectangle(0.5, 0.5, .5, .5) # Recall that (x,y) denote CENTER of rectangle
    qt = QuadTree(boundary=rect, capacity=4)

    # Create points
    N = 100  # Number of points to draw
    rng = default_rng()  # Random number generator
    points = [Point(rng.random(), rng.random()) for _ in range(N)]

    # Pass points into QuadTree
    for p in points:
        qt.InsertPoint(p)

    # Establish figure
    fig, ax = plt.subplots()

    # Draw points
    X, Y = [p.x for p in points], [p.y for p in points]
    #ax.scatter(X, Y, c="w", s=4)

    # Draw QuadTree
    qt.DrawOutline(ax)

    #### Beautification ####
    ax.set_facecolor("k")
    plt.xticks([])
    plt.yticks([])
    plt.xlim([qt.boundary.x - qt.boundary.w, qt.boundary.x + qt.boundary.w])
    plt.ylim([qt.boundary.y - qt.boundary.h, qt.boundary.y + qt.boundary.h])
    plt.show()
    return

if __name__ == "__main__":
    draw()

