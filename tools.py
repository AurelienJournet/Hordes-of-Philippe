from math import sqrt
from typing import List, Set

import pygame


def calculate_distance_between_points(point_a: tuple, point_b: tuple) -> float:
    return sqrt((point_a[0]-point_b[0])**2 + (point_a[1]-point_b[1])**2)


def does_vector_collide_rects(vector_start: tuple, vector_end: tuple, rects_list: List[pygame.Rect]) -> float:

    # TODO : documenter : retourne la distance avec le rectangle collisionné le plus proche (distance par rapport au vector_start
    # TODO : ainsi, on pourra savoir par exemple si le vecteur a touché un mur avant de toucher un ennemi
    # TODO : retourne -1 si pas de collision

    min_dist = -1
    # print(vector_start, vector_end)
    for rect in rects_list:
        for points_couple in [(rect.topleft, rect.topright), (rect.topright, rect.bottomright),
                              (rect.bottomright, rect.bottomleft), (rect.bottomleft, rect.topleft)]:
            rect_vect = [points_couple[0], points_couple[1]]

            if do_the_vectors_intersect([vector_start, vector_end], rect_vect):
                rect_vect_center = ((rect_vect[0][0] + rect_vect[1][0])/2, (rect_vect[0][1] + rect_vect[1][1])/2)

                distance_between_points = calculate_distance_between_points(vector_start, rect_vect_center)
                if min_dist == -1 or distance_between_points < min_dist:
                    min_dist = distance_between_points

    return min_dist


def do_the_vectors_intersect(vector_a: List[tuple], vector_b: List[tuple]) -> bool:

    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    # Given three collinear points p, q, r, the function checks if
    # point q lies on line segment 'pr'
    def on_segment(p: Point, q: Point, r: Point):
        if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
        (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
            return True

        return False

    def orientation(p: Point, q: Point, r: Point):
        # to find the orientation of an ordered triplet (p,q,r)
        # function returns the following values:
        # 0 : Collinear points
        # 1 : Clockwise points
        # 2 : Counterclockwise
        # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
        # for details of below formula.
        val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
        if val > 0:
            # Clockwise orientation
            return 1
        elif val < 0:
            # Counterclockwise orientation
            return 2
        else:
            # Collinear orientation
            return 0

    # The main function that returns true if
    # the line segment 'p1q1' and 'p2q2' intersect.
    def do_intersect(p1: Point, q1: Point, p2: Point, q2: Point):

        # Find the 4 orientations required for
        # the general and special cases
        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        # General case
        if (o1 != o2) and (o3 != o4):
            return True
        # Special Cases
        # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
        if (o1 == 0) and on_segment(p1, p2, q1):
            return True
        # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
        if (o2 == 0) and on_segment(p1, q2, q1):
            return True
        # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
        if (o3 == 0) and on_segment(p2, p1, q2):
            return True

        # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
        if (o4 == 0) and on_segment(p2, q1, q2):
            return True

        # If none of the cases
        return False

    p1 = Point(vector_a[0][0], vector_a[0][1])
    p2 = Point(vector_b[0][0], vector_b[0][1])
    q1 = Point(vector_a[1][0], vector_a[1][1])
    q2 = Point(vector_b[1][0], vector_b[1][1])

    return do_intersect(p1, q1, p2, q2)
