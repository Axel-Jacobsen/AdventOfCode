#! /usr/bin/env python3


def get_prog(fname):
    with open(fname, 'r') as f:
        return [int(s) for s in f.readline().strip().split(',')]

def opcode(r: list):
    f = list(r)
    pc = 0

    def get_v(v, parameter_mode):
        if parameter_mode == 0: # position mode
            return f[f[v]]
        if parameter_mode == 1: # immediate mode
            return f[v]
        raise RuntimeError(f'Unexpected parameter mode: {parameter_mode}')

    def gord(arr, v):
        if v < len(arr):
            return int(arr[v])
        else:
            return 0

    while True:
        opcode = str(f[pc])[-2:]

        if len(opcode) == 1:
            opcode = '0' + opcode

        pms = str(f[pc])[:-2][::-1]

        if opcode == '01':
            f[f[pc + 3]] = get_v(pc + 1, gord(pms, 0)) + get_v(pc + 2, gord(pms, 1))
            pc += 4

        elif opcode == '02':
            f[f[pc + 3]] = get_v(pc + 1, gord(pms, 0)) * get_v(pc + 2, gord(pms, 1))
            pc += 4

        elif opcode == '03':
            f[f[pc + 1]] = int(input('> '))
            pc += 2

        elif opcode == '04':
            print(get_v(pc + 1, gord(pms, 0)))
            pc += 2

        elif opcode == '05':
            # Jump if not zero
            if get_v(pc + 1, gord(pms, 0)) != 0:
                pc = get_v(pc + 2, gord(pms, 1))
            else:
                pc += 3

        elif opcode == '06':
            # Jump if zero
            if get_v(pc + 1, gord(pms, 0)) == 0:
                pc = get_v(pc + 2, gord(pms, 1))
            else:
                pc += 3

        elif opcode == '07':
            # Less than
            if get_v(pc + 1, gord(pms, 0)) < get_v(pc + 2, gord(pms, 1)):
                f[f[pc + 3]] = 1
            else:
                f[f[pc + 3]] = 0
            pc += 4

        elif opcode == '08':
            # Less than
            if get_v(pc + 1, gord(pms, 0)) == get_v(pc + 2, gord(pms, 1)):
                f[f[pc + 3]] = 1
            else:
                f[f[pc + 3]] = 0
            pc += 4

        elif opcode == '99':
            # Program is done
            break

        else:
            # Illegal Opcode
            # Or something else is wrong
            raise RuntimeError(f'Illegal Opcode {opcode} | PC {pc}')

    return f


if __name__ == '__main__':
    f  = get_prog('prog.txt')
    mf = opcode(f)

