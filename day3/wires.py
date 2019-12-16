#! /usr/bin/env python3

def get_paths(fname):
    with open(fname, 'r') as f:
        l1 = tuple(f.readline().strip().split(','))
        l2 = tuple(f.readline().strip().split(','))
        return (l1, l2)

def get_crosses():
    pass

def dist():
    path1, path2 = get_paths('paths.txt')

if __name__ == '__main__':
    print(get_paths('paths.txt'))
    get_crosses()
    dist()

