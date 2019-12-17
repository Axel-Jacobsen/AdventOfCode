#! /usr/bin/env python3
import re

"""
Password Traits:
    It is a six-digit number.
    The value is within the range given in your puzzle input.
    Two adjacent digits are the same (like 22 in 122345).
    Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:
    111111 meets these criteria (double 11, never decreases).
    223450 does not meet these criteria (decreasing pair of digits 50).
    123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet these criteria?

IN: 264793-803935.
"""

def none_decreasing(num):
    digits = [int(c) for c in str(num)]
    dp = digits[0]
    for i in range(1, len(digits)):
        if digits[i] < dp:
            return False
        dp = digits[i]
    return True

def same(num):
    s = str(num)
    letter_list = [m.group(0) for m in re.finditer(r"(\d)\1*", s)]
    for l in letter_list:
        if len(l) == 2:
            return True
    return False

def crack_count(start, end):
    cnt = 0
    for i in range(start, end):
        if (none_decreasing(i) and same(i)):
            cnt += 1
    return cnt


if __name__ == '__main__':
    cnt = crack_count(264793, 803935)
    print(cnt)

