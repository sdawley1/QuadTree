"""
Algorithm to find the closest two schools in VT in O(nlogn)
"""
import math
import numpy as np
import pandas as pd
import sys
import time

sys.path.insert(0, "..")
from qtree.quad_tree import Point, QuadTree, Rectangle

def get_points(df) -> list:
    """
    Get points from VT data frame
    :param df: pd.DataFrame()
    :return:
    """
    points = []
    for x, y in zip(df["X"], df["Y"]):
        points.append(Point(x, y))
    return points

def load_VT_schools(filename) -> pd.DataFrame():  # What
    """
    :return:
    """
    return pd.read_csv(filename, sep=",")

def GetClosestSchools(qt, schools) -> tuple:
    """
    Get two closest schools using QuadTree
    :param qt: (QuadTree) QuadTree to get schools from
    :param schools: (list) List of schools with .x, .y, and .name attributes
    :return:
    """
    running_min = (np.inf, None, None)
    for school in schools:
        if qt.boundary.ContainsPoint(school):  # Test if point is contained within QuadTree boundary
            for spt in qt.QueryRegion(qt.boundary):  # Find all points within the QuadTree boundary
                for ospt in qt.QueryRegion(qt.boundary):  # Find all other points within the QuadTree boundary
                    if spt != ospt:
                        eu_dist = math.dist((spt.x, spt.y), (ospt.x, ospt.y))
                        if eu_dist < running_min[0]:
                            running_min = (eu_dist, spt, ospt)

    return running_min

def closest_main() -> tuple:
    """
    Find two closest schools in VT
    :return:
    """
    # Get elapsed time
    t_start = time.process_time()
    # Load data
    df = load_VT_schools("../data/VT_schools.txt")

    # First we create a list of all schools in the state
    # Don't mind the fact that the "Organization" was misspelled in the csv file
    schools = []
    for x, y, name in zip(df["X"], df["Y"], df["ORGANIZATI"]):
        schools.append(Point(x, y, name))

    # Feed this data into a QuadTree
    # Firstly, we'll grab the mins/maxes from the spatial data to define the boundary of the QuadTree
    x_min, x_max, y_min, y_max = df["X"].min(), df["X"].max(), df["Y"].min(), df["Y"].max()
    # = 433215.1900730124,  575880.7324778801, 28462.516662897546, 277983.900319282
    boundary = Rectangle(
        (x_min + x_max) / 2,
        (y_min + y_max) / 2,
        np.absolute((x_min + x_max) / 2 - x_max / 1.4),  # FIX THIS
        np.absolute((y_min + y_max) / 2 + y_max / 15)  # FIX THIS
    )
    # Define and add points to QuadTree
    qt = QuadTree(boundary, capacity=4)
    for school in schools:
        qt.InsertPoint(school)

    # Main loop to get closest points
    closest = GetClosestSchools(qt, schools)

    t_end = time.process_time()
    return closest, (t_end - t_start)

if __name__ == "__main__":
    res, s = closest_main()
    print(f"{res[1].name} and {res[2].name} are the two closest schools, separated by {res[0]} units.")
    # Peoples Academy and Peoples Academy Middle School are the two closest schools, separated by 18.5209 units.
    print(f"Total elapsed time: {s} s")
    # 43.392189 s
