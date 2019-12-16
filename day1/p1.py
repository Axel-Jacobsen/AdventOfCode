#! /usr/bin/env python3

def part1():
    tot = 0
    with open('input.txt', 'r') as f:
        for line in f:
            mass = int(line.strip())
            tot += mass // 3 - 2
    return tot

def part2():
    tot = 0
    with open('input.txt', 'r') as f:
        for line in f:
            curr_fuel = 0
            mass = int(line.strip())
            newfuel = mass // 3 - 2
            while newfuel > 0:
                curr_fuel += newfuel
                newfuel = newfuel // 3 - 2
            tot += curr_fuel
    return tot

if __name__ == '__main__':
    print(f'PART 1: {part1()}')
    print(f'PART 2: {part2()}')

