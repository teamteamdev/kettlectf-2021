from collections import deque
import time


class Registers(dict):
    def __init__(self, registers):
        self.registers = registers
        super().__init__()
        for letter in registers:
            self[letter] = 0

    def __missing__(self, key):
        return int(key)

    def __contains__(self, key):
        return key in self.registers


class Ram(list):
    def __init__(self, size):
        self.size = size
        self.reset_state()

    def reset_state(self):
        super().__init__([0] * self.size)

    def __contains__(self, i):
        return i in range(self.size)


class Code:
    def __init__(self, labels, instructions, registers):
        self.instructions = instructions
        self.labels = labels
        self.registers = registers

    @classmethod
    def compile(cls, code, registers='abcd'):
        def check(arg):
            if not arg:
                return False
            if arg[0] == '-' and arg[1:].isdigit():
                return True
            if arg.isdigit():
                return True
            return arg in registers

        labels = {}
        lines = deque(line.strip() for line in code.splitlines())
        instuctions = []
        defines = {}
        defines_count = {}
        used_labels = set()
        while lines:
            line = lines.popleft().lower()
            if not line:
                continue
            if line.endswith('!'):
                name = line[:-1]
                content = defines.get(name)
                if not content:
                    return None
                label_prefix = f'{name}-{defines_count[name]}#'
                for l in content:
                    if l.endswith(':'):
                        l = label_prefix + l
                    elif '{}' in l:
                        if l.count('{}') > 1:
                            return None
                        l = l.format(label_prefix)
                    lines.appendleft(l)
                defines_count[name] += 1
            elif line.startswith('#define'):
                line = line.split()
                if len(line) != 2:
                    return None
                _, name = line
                if name in defines:
                    return None
                content = []
                bad_line = f'{name}!'
                while lines:
                    n = lines.popleft()
                    if n == '#enddefine':
                        break
                    elif n == bad_line:
                        return None
                    content.append(n)
                defines[name] = list(reversed(content))
                defines_count[name] = 0
            elif line == '#enddefine':
                return None
            elif line.endswith(':'):
                label = line[:-1]
                if len(label.split()) != 1 or label in labels:
                    return None
                labels[label] = len(instuctions)
            else:
                cmd, *args = line.split()
                if cmd in ('push', 'pop'):
                    if len(args) != 1:
                        return None
                    arg = args[0]
                    if cmd.startswith('pop') and arg not in registers:
                        return None
                    elif not check(arg):
                        return None
                    instuctions.append((cmd, arg, None))
                elif cmd in ('jl', 'je'):
                    if len(args) != 2:
                        return None
                    arg, label = args
                    if not check(arg):
                        return None
                    if not (label[0] == label[-1] == '"'):
                        return None
                    label = label[1:-1]
                    used_labels.add(label)
                    instuctions.append((cmd, arg, label))
                elif cmd in ('add', 'sub'):
                    if len(args) != 2:
                        return None
                    arg, arg2 = args
                    if arg not in registers or not check(arg2):
                        return None
                    instuctions.append((cmd, arg, arg2))
                elif cmd == 'save':
                    if len(args) != 2:
                        return None
                    addr, val = args
                    if not check(addr) or not check(val):
                        return None
                    instuctions.append((cmd, addr, val))
                elif cmd == 'load':
                    if len(args) != 2:
                        return None
                    addr, dest = args
                    if not check(addr) or dest not in registers:
                        return None
                    instuctions.append((cmd, addr, dest))
                else:
                    return None
        for label in used_labels:
            if not label in labels:
                return None
        return cls(labels, instuctions, registers)


class VM:
    def __init__(self, code, ram):
        self.code = code
        self.ram = ram
        self.reset_state()

    def reset_state(self):
        self.stack = []
        self.ram.reset_state()
        self.registers = Registers(self.code.registers)

    def run(self, timeout=1):
        start = time.monotonic()
        ins = self.code.instructions
        labels = self.code.labels
        cnt = pos = 0
        self.stack.append(self.ram.size)
        while pos < len(ins):
            cmd, a, b = ins[pos]
            if cmd == 'push':
                self.stack.append(self.registers[a])
            elif cmd == 'pop':
                if not self.stack:
                    return -1
                self.registers[a] = self.stack.pop()
            elif cmd == 'add':
                self.registers[a] += self.registers[b]
            elif cmd == 'sub':
                self.registers[a] -= self.registers[b]
            elif cmd == 'load':
                addr = self.registers[a]
                if addr not in self.ram:
                    return -1
                self.registers[b] = self.ram[addr]
            elif cmd == 'save':
                addr = self.registers[a]
                if addr not in self.ram:
                    return -1
                self.ram[addr] = self.registers[b]
            elif cmd == 'je':
                if self.registers[a] == 0:
                    pos = labels[b] - 1
            elif cmd == 'jl':
                if self.registers[a] < 0:
                    pos = labels[b] - 1
            pos += 1
            cnt += 1
            if timeout and time.monotonic() - start > timeout:
                return -1
        return cnt


if __name__ == '__main__':
    import sys
    code = sys.stdin.read()
    code = Code.compile(code)
    if not code:
        print('Compilation error', file=sys.stderr)
        sys.exit(1)
    vm = VM(code, Ram(128))
    vm.stack = [int(arg) for arg in sys.argv[1:]]
    res = vm.run(0)
    if res == -1:
        print('Runtime error', file=sys.stderr)
        sys.exit(2)
    print('Cycles count', res)
    n = len(vm.stack)
    for i, v in enumerate(vm.stack):
        print(v, f'({n - i})')
