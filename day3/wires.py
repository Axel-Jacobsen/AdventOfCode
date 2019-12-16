#! /usr/bin/env python3

from collections import namedtuple

Pos = namedtuple('Pos', ('x', 'y'))


class Wire(object):

    def __init__(self, p1, p2, path_length):
        """ low and start are named tuples
        """
        self.start = p1
        self.end = p2
        self.path_length = path_length
        self.is_vertical = (p1.x == p2.x)
        self.x = p1.x if self.is_vertical else None
        self.y = p2.y if not self.is_vertical else None

    def __repr__(self):
        return f'Wire({self.start.x, self.start.y},{self.end.x, self.end.y})'

    def intersects(self, other):
        """ Returns (x,y) pos if intersects, and None otherwise
        """
        # If wires are parallel, no intersections
        if self.is_vertical == other.is_vertical:
            assert not ((self.x == other.x and self.x != 0 and self.x is not None)
                    or (self.y == other.y and self.y != 0 and self.y is not None)), 'coincident lines encountered'
            return None

        other_low_x, other_high_x, other_low_y, other_high_y = Wire.bounding_points(other)
        self_low_x, self_high_x, self_low_y, self_high_y = Wire.bounding_points(self)

        # Check this line being vertical and other horizontal
        if self.is_vertical:
            if (other_low_x <= self.x <= other_high_x and self_low_y <= other.y <= self_high_y):
                return Pos(self.x, other.y)
        else:
            if (other_low_y <= self.y <= other_high_y and self_low_x <= other.x <= self_high_x):
                return Pos(other.x, self.y)

        return None

    @staticmethod
    def bounding_points(w):
        return (min(w.start.x, w.end.x), max(w.start.x, w.end.x), min(w.start.y, w.end.y), max(w.start.y, w.end.y))


def get_paths(fname):
    with open(fname, 'r') as f:
        l1 = tuple(f.readline().strip().split(','))
        l2 = tuple(f.readline().strip().split(','))
        return (l1, l2)

def path_to_wires(directions):
    wire_set = []
    curr_x, curr_y = 0, 0
    path_length = 0
    for dirx in directions:
        if dirx[0] == 'U':
            wire_set.append(
                    Wire(
                        Pos(curr_x, curr_y),
                        Pos(curr_x, curr_y + int(dirx[1:])),
                        path_length
                        )
                    )
            curr_x, curr_y = curr_x, curr_y + int(dirx[1:])
        elif dirx[0] == 'D':
            wire_set.append(
                    Wire(
                        Pos(curr_x, curr_y),
                        Pos(curr_x, curr_y - int(dirx[1:])),
                        path_length
                        )
                    )
            curr_x, curr_y = curr_x, curr_y - int(dirx[1:])
        elif dirx[0] == 'L':
            wire_set.append(
                    Wire(
                        Pos(curr_x, curr_y),
                        Pos(curr_x - int(dirx[1:]), curr_y),
                        path_length
                        )
                    )
            curr_x, curr_y = curr_x - int(dirx[1:]), curr_y
        elif dirx[0] == 'R':
            wire_set.append(
                    Wire(
                        Pos(curr_x, curr_y),
                        Pos(curr_x + int(dirx[1:]), curr_y),
                        path_length
                        )
                    )
            curr_x, curr_y = curr_x + int(dirx[1:]), curr_y
        path_length += int(dirx[1:])
    return wire_set

def point_distance(p1, p2):
    return abs(p2.x - p1.x) + abs(p2.y - p1.y)

def get_manhattan_dist(fname):
    path1, path2 = get_paths(fname)
    wireset1 = path_to_wires(path1)
    wireset2 = path_to_wires(path2)
    min_dist = 1000000
    for w1 in wireset1:
        for w2 in wireset2:
            cross = w1.intersects(w2)
            if not cross:
                continue
            d = point_distance(cross, Pos(0,0))
            if d < min_dist and d != 0:
                min_dist  = d 

    return min_dist

def get_path_dist(fname):
    path1, path2 = get_paths(fname)
    wireset1 = path_to_wires(path1)
    wireset2 = path_to_wires(path2)
    min_pathlen = 1000000
    for w1 in wireset1:
        for w2 in wireset2:
            cross = w1.intersects(w2)
            if not cross:
                continue
            d = point_distance(cross, Pos(0,0))
            pathlen = w1.path_length + point_distance(w1.start, cross) + \
                      w2.path_length + point_distance(w2.start, cross)
            if pathlen < min_pathlen and d != 0:
                min_pathlen = pathlen
    return min_pathlen

if __name__ == '__main__':
    v1 = get_path_dist('testp1.txt')
    v2 = get_manhattan_dist('testp1.txt')
    v3 = get_path_dist('testp2.txt') 
    v4 = get_manhattan_dist('testp2.txt')
    print(v1, '<-', 610)
    print(v2, '<-', 159)
    print(v3, '<-', 410)
    print(v4, '<-', 135)

    min_dist = get_manhattan_dist('paths.txt')
    pathlen = get_path_dist('paths.txt')
    print('FINAL MANHATTAN DISTANCE:', min_dist)
    print('SUM OF PATH LENGTHS:     ', pathlen)

