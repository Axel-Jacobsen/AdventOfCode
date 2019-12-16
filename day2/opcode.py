#! /usr/bin/env python3


def get_prog(fname):
    with open(fname, 'r') as f:
        p = f.readline().strip()
        return list(map(lambda s: int(s), p.split(',')))

def opcode(r: list):
    f = list(r)
    program_counter = 0
    while True:
        if f[program_counter] == 1:
            f[f[program_counter + 3]] = f[f[program_counter + 1]] + \
                                        f[f[program_counter + 2]]
            program_counter += 4

        elif f[program_counter] == 2:
            f[f[program_counter + 3]] = f[f[program_counter + 1]] * \
                                        f[f[program_counter + 2]]
            program_counter += 4

        elif f[program_counter] == 99:
            # Program is done
            break

        else:
            # Illegal Opcode
            # Or something else is wrong
            raise RuntimeError(f'Illegal Opcode: {f[program_counter]}')

    return f


if __name__ == '__main__':
    f  = get_prog('prog.txt')
    mf = opcode(f)

    # Part 2
    # Goal: f[0] = 19690720
    # modify the program `f` by
    # changing f[1] (noun) and f[2] (verb)
    # return 100 * noun + verb
    for i in range(100):
        for j in range(100):
            f[1] = i
            f[2] = j
            mf = opcode(f)

            if mf[0] == 19690720:
                print(100 * i + j)
                break

