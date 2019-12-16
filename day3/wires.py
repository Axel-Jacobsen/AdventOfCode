#! /usr/bin/env python3

from collections import namedtuple

Pos = namedtuple('Pos', ('x', 'y'))


class Wire(object):

    def __init__(self, p1, p2):
        """ low and start are named tuples
        """
        self.start = p1
        self.end = p2
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
            assert not ((self.x == other.x and self.x != 0 and self.x is not None) or (self.y == other.y and self.y != 0 and self.y is not None)), 'coincident lines encountered'
            return None

        other_low_x  = min(other.start.x, other.end.x)
        other_high_x = max(other.start.x, other.end.x)
        other_low_y  = min(other.start.y, other.end.y)
        other_high_y = max(other.start.y, other.end.y)
        self_low_x  = min(self.start.x, self.end.x)
        self_high_x = max(self.start.x, self.end.x)
        self_low_y  = min(self.start.y, self.end.y)
        self_high_y = max(self.start.y, self.end.y)

        # Check this line being vertical and other horizontal
        if self.is_vertical:
            if (other_low_x <= self.x <= other_high_x
                and self_low_y <= other.y <= self_high_y):
                return Pos(self.x, other.y)
        else:
            if (other_low_y <= self.y <= other_high_y
                and self_low_x <= other.x <= self_high_x):
                return Pos(other.x, self.y)

        return None


def get_paths(fname):
    with open(fname, 'r') as f:
        l1 = tuple(f.readline().strip().split(','))
        l2 = tuple(f.readline().strip().split(','))
        return (l1, l2)

def path_to_wires(directions):
    wire_set = []
    curr_x, curr_y = 0, 0
    for dirx in directions:
        if dirx[0] == 'U':
            wire_set.append(Wire(Pos(curr_x, curr_y), Pos(curr_x, curr_y + int(dirx[1:]))))
            curr_x, curr_y = curr_x, curr_y + int(dirx[1:])
        elif dirx[0] == 'D':
            wire_set.append(Wire(Pos(curr_x, curr_y), Pos(curr_x, curr_y - int(dirx[1:]))))
            curr_x, curr_y = curr_x, curr_y - int(dirx[1:])
        elif dirx[0] == 'L':
            wire_set.append(Wire(Pos(curr_x, curr_y), Pos(curr_x - int(dirx[1:]), curr_y)))
            curr_x, curr_y = curr_x - int(dirx[1:]), curr_y
        elif dirx[0] == 'R':
            wire_set.append(Wire(Pos(curr_x, curr_y), Pos(curr_x + int(dirx[1:]), curr_y )))
            curr_x, curr_y = curr_x + int(dirx[1:]), curr_y
    return wire_set

def dist(fname):
    path1, path2 = get_paths(fname)
    wireset1 = path_to_wires(path1)
    wireset2 = path_to_wires(path2)
    min_dist = 1000000
    for w1 in wireset1:
        for w2 in wireset2:
            cross = w1.intersects(w2)
            assert cross == w2.intersects(w1)
            if cross:
                min_dist = min(min_dist, abs(cross.x) + abs(cross.y)) if (cross.x != 0 and cross.y != 0) else min_dist

    return min_dist


if __name__ == '__main__':
    print('FINAL:', dist('paths.txt'))

