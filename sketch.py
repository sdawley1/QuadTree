"""
QuadTrees!
"""
import numpy as np
from numpy.random import default_rng
import matplotlib.pyplot as plt
from qtree.quad_tree import Point, QuadTree, Rectangle
from schools.get_closest import get_points, load_VT_schools, GetClosestSchools


def draw() -> None:
    """
    Draw all elements of matplotlib figure
    """
    # Establish QuadTree
    rect = Rectangle(0.5, 0.5, .5, .5) # Recall that (x,y) denote CENTER of rectangle
    qt = QuadTree(boundary=rect, capacity=4)

    # Create points
    N = 750  # Number of points to draw
    rng = default_rng()  # Random number generator
    points = [Point(rng.random(), rng.random()**3) for _ in range(N)]

    # Pass points into QuadTree
    for p in points:
        qt.InsertPoint(p)

    # Establish figure
    fig, ax = plt.subplots()

    # Draw points
    X, Y = [p.x for p in points], [p.y for p in points]
    ax.scatter(X, Y, c="r", s=4)

    # Draw QuadTree
    qt.DrawOutline(ax)

    # Create region to query points
    q_region = Rectangle(
        rng.uniform(0.3, 0.7), rng.uniform(0.3, 0.7),
        rng.uniform(0.1, 0.2), rng.uniform(0.1, 0.2)
    )
    q_region.DrawOutline(ax)
    # Color points within region defined above
    found_points = qt.QueryRegion(q_region)
    for p in found_points:
        ax.scatter(p.x, p.y, c="#0CFF00", s=4)

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
        schools.append(Point(x, y, name))

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
        qt.InsertPoint(school)

    closest = GetClosestSchools(qt, schools)

    # Establish figure
    fig, ax = plt.subplots()

    # Draw points
    X, Y = [p.x for p in get_points(df)], [p.y for p in get_points(df)]
    ax.scatter(X, Y, c="r", s=8)
    # Highlight closest schools
    ax.scatter([closest[1].x, closest[2].x], [closest[1].y, closest[2].y], c="#0CFF00", s=8)

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

