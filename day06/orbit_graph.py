#! /usr/bin/env python3
# VIS: (echo 'digraph G {' && sed 's/^/"/g;s/)/"->"/g;s/$/"/g' map && echo '}') | dot -Tsvg -o out.svg

from functools import reduce

class Planet(object):

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.sats = set()

    def __repr__(self):
        return self.name

    def graph(self, level=0, spacing='\t'):
        preprint = level * spacing 
        print(f'{preprint}|{self.name}')
        for child in self.sats:
            child.graph(level + 1)

    def size(self):
        return 1 + reduce(
                lambda x,y: x+y, [child.size() for child in self.sats], 0
            )

    def norbits(self, n=0):
        return n + reduce(
                lambda x,y: x+y, [child.norbits(n + 1) for child in self.sats], 0
            )

def dist_to(NOI, name, n=0):
    # print(' ' * n, f'{NOI.name} {n} {[s.name for s in NOI.sats]}')
    for node in NOI.sats:
        if node.name == name:
            return n
        else:
            out = dist_to(node, name, n + 1)
            if out != -1:
                return out
    return -1


def get_named(NOI, name):
    # print(' ' * n, f'{NOI.name} {n} {[s.name for s in NOI.sats]}')
    for node in NOI.sats:
        if node.name == name:
            return node
        else:
            out = get_named(node, name)
            if out.name != None:
                return out
    return Planet(None)

def parents(NOI):
    l=[]
    v = NOI
    while v.parent is not None:
        v = v.parent
        l.append(v)
    return l

def xfers(root, start, end):
    d1 = parents(get_named(root, start))
    d2 = parents(get_named(root, end))
    for el in d1:
        try:
            ind = d2.index(el)
            break
        except ValueError:
            pass
    return ind + d1.index(el)

def create_graph(NOI, orbit_data):
    for orb in orbit_data:
        if NOI.name == orb[0]:
            p = Planet(orb[1], NOI)
            create_graph(p, orbit_data)
            NOI.sats.add(p)

def get_orbit_data(fname):
    orbits = []
    with open(fname, 'r') as f:
        for line in f:
            orbits.append(
                tuple(map(lambda s: s.strip(), line.split(')')))
                )
    return orbits


if __name__ == '__main__':
    orbit_data = get_orbit_data('map')
    NOI = Planet('COM')
    create_graph(NOI, orbit_data)
    print(xfers(NOI, 'YOU', 'SAN'))

