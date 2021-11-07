import sys

table = {
    '<': 1,
    '>': 2,
    '+': 3,
    '-': 4,
    '.': 5,
    ',': 6,
    '[': 7,
    ']': 8,
}


def convert(prog):
    return [table[c] for c in prog]


if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            prog = f.read()
    else:
        prog = sys.stdin.read()
    prog = ''.join(prog.splitlines())
    print(*convert(prog))
