"""
QuadTrees!
"""
from csv import QUOTE_ALL
import numpy as np
from numpy import random
from numpy.random import default_rng
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from geometry.shapes import Particle, Rectangle
from qtree.quad_tree import QuadTree
from schools.get_closest import get_points, load_VT_schools, get_closest_schools

def draw() -> None:
    """
    """
    fig, ax = plt.subplots(figsize=(8,8))
    ax.set_facecolor("k")

    # QuadTree + drawing boundaries
    qt_bound = Rectangle(0.5, 0.5, 0.5, 0.5)
    qt = QuadTree(qt_bound, capacity=4)

    # Generate points and plot
    points = []
    for i in range(100):
        p = Particle(random.rand(1)/1.2, random.rand(1)/1.2, 0.01)
        points.append(p)
        p.draw_outline(ax, c="w")
        qt.insert_point(p)

    # Draw outline of QuadTree after inserting points
    #qt.DrawOutline(ax, c="w")

    # Test collisions
    # THIS HAS ISSUES
    for pt in points:
        found = qt.query_region(pt)
        for opt in found:
            if pt != opt and pt.intersects_region(opt):
                pt.draw_outline(ax, c="r", ec="r")
            
    ### Beautification ###
    plt.xticks([])
    plt.yticks([])
    plt.xlim([qt.boundary.x - qt.boundary.w, qt.boundary.x + qt.boundary.w])
    plt.ylim([qt.boundary.y - qt.boundary.h, qt.boundary.y + qt.boundary.h])
    plt.savefig("images/first_collisions2.png")
    plt.show()
    return

def drawQT() -> None:
    """
    Draw all elements of matplotlib figure
    """
    # Establish QuadTree
    rect = Rectangle(0.5, 0.5, .5, .5) # Recall that (x,y) denote CENTER of rectangle
    qt = QuadTree(boundary=rect, capacity=4)

    # Create points
    N = 750  # Number of points to draw
    rng = default_rng()  # Random number generator
    points = [Particle(rng.random(), rng.random()**3, 0.25) for _ in range(N)]

    # Pass points into QuadTree
    for p in points:
        qt.insert_point(p)

    # Establish figure
    fig, ax = plt.subplots(figsize=(6, 6))

    # Draw points
    X, Y = [p.x for p in points], [p.y for p in points]
    ax.scatter(X, Y, c="r", s=4)

    # Draw QuadTree
    qt.draw_outline(ax)

    # Create region to query points
    q_region = Rectangle(
        rng.uniform(0.3, 0.7), rng.uniform(0.3, 0.7),
        rng.uniform(0.1, 0.2), rng.uniform(0.1, 0.2)
    )
    q_region.draw_outline(ax)
    # Color points within region defined above and test collisions
    for p in qt.query_region(q_region):
        ax.scatter(p.x, p.y, c="w", s=4)
        found = qt.query_region(p)
        for other_p in found:
            if p is not other_p and p.intersects_region(other_p):
                p.draw_outline(ax, c="#0CFF00")


    # # Test collisions
    # # THIS HAS ISSUES
    # for pt in points:
    #     found = qt.QueryRegion(pt)
    #     for opt in found:
    #         if pt != opt and pt.IntersectsRegion(opt):
    #             pt.DrawOutline(ax, c="r", ec="r")

    #### Beautification ####
    ax.set_facecolor("k")
    plt.xticks([])
    plt.yticks([])
    plt.xlim([qt.boundary.x - qt.boundary.w, qt.boundary.x + qt.boundary.w])
    plt.ylim([qt.boundary.y - qt.boundary.h, qt.boundary.y + qt.boundary.h])
    plt.show()

    return

def drawVT() -> None:
    """
    Plot locations of all schools in VT within matplotlib figure
    {
    Min x-value: 433215.1900730124
    Max x-value: 575880.7324778801
    Min y-value: 277983.900319282
    Max y-value: 28462.516662897546
    }
    """
    # Load VT data
    df = load_VT_schools("data/VT_schools.txt")
    # Get minimums and maximums for figure dimensions
    x_min = df["X"].min()  # 433215.1900730124
    x_max = df["X"].max()  # 575880.7324778801
    y_min = df["Y"].min()  # 28462.516662897546
    y_max = df["Y"].max()  # 277983.900319282

    # Get list of schools
    schools = []
    for x, y, name in zip(df["X"], df["Y"], df["ORGANIZATI"]):
        schools.append(Particle(x, y, name))

    # Build QuadTree
    # Recall that (x,y) denote CENTER of rectangle
    rect = Rectangle(
        (x_min + x_max) / 2,
        (y_min + y_max) / 2,
        np.absolute((x_min + x_max) / 2 - x_max / 1.4),
        np.absolute((y_min + y_max) / 2 + y_max / 15)
    )
    qt = QuadTree(boundary=rect, capacity=4)

    # Pass points into QuadTree
    for school in schools:
        qt.insert_point(school)

    closest = get_closest_schools(qt, schools)

    # Establish figure
    fig, ax = plt.subplots()

    # Draw points
    X, Y = [p.x for p in get_points(df)], [p.y for p in get_points(df)]
    ax.scatter(X, Y, c="r", s=8)
    # Highlight closest schools
    ax.scatter([closest[1].x, closest[2].x], [closest[1].y, closest[2].y], c="#0CFF00", s=8)

    # Draw QuadTree
    qt.draw_outline(ax)

    #### Beautification ####
    ax.set_facecolor("k")
    plt.xticks([])
    plt.yticks([])
    plt.xlim([qt.boundary.x - qt.boundary.w, qt.boundary.x + qt.boundary.w])
    plt.ylim([qt.boundary.y - qt.boundary.h, qt.boundary.y + qt.boundary.h])
    plt.show()
    return

if __name__ == "__main__":
    #drawQT() 
    rng = default_rng()
    # Define points in space and QuadTree
    rect = Rectangle(x=0.5, y=0.5, w=0.5, h=0.5)
    qt = QuadTree(boundary=rect, capacity=4)
    # Inserting points into the QuadTree
    for _ in range(400):
        x, y, r = rng.uniform(), rng.uniform(), rng.uniform()
        qt.insert_point(Particle(x, y, r))
    
    # Display QuadTree
    qt.quad_tree_display()


