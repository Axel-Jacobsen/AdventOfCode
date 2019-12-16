#! /usr/bin/env python3

tot = 0

with open('input.txt', 'r') as f:
    for line in f:
        mass = int(line.strip())
        fuel = mass // 3 - 2
        print(fuel)
        tot += fuel

print(f'TOTAL: {tot}')

