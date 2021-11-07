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


class VM:
    def __init__(self, code):
        self.error = False
        self.reset_state()
        self._compile(code)

    def reset_state(self):
        self.stack = []
        self.registers = Registers('abcd')

    def run(self, timeout=1):
        if self.error:
            return
        cnt = 0
        pos = 0
        start = time.monotonic()
        while pos < len(self.code):
            cmd, a, b = self.code[pos]
            if cmd == 'push':
                self.stack.append(self.registers[a])
            elif cmd == 'pop':
                if not self.stack:
                    self.error = True
                    return
                self.registers[a] = self.stack.pop()
            elif cmd == 'add':
                self.registers[a] += self.registers[b]
            elif cmd == 'sub':
                self.registers[a] -= self.registers[b]
            elif cmd == 'je':
                if self.registers[a] == 0:
                    pos = self._labels[b] - 1
            elif cmd == 'jl':
                if self.registers[a] < 0:
                    pos = self._labels[b] - 1
            if timeout and time.monotonic() - start > timeout:
                self.error = True
                return
            pos += 1
            cnt += 1
        return cnt

    def _compile(self, code):
        def check(arg):
            if not arg:
                return False
            if arg[0] == '-' and arg[1:].isdigit():
                return True
            if arg.isdigit():
                return True
            return arg in self.registers

        self._labels = {}
        lines = deque(line.strip() for line in code.splitlines())
        self.code = []
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
                    self.error = True
                    return
                label_prefix = f'{name}-{defines_count[name]}#'
                for l in content:
                    if l.endswith(':'):
                        l = label_prefix + l
                    elif '{}' in l:
                        if l.count('{}') > 1:
                            self.error = True
                            return
                        l = l.format(label_prefix)
                    lines.appendleft(l)
                defines_count[name] += 1
            elif line.startswith('#define'):
                line = line.split()
                if len(line) != 2:
                    self.error = True
                    return
                _, name = line
                if name in defines:
                    self.error = True
                    return
                content = []
                bad_line = f'{name}!'
                while lines:
                    n = lines.popleft()
                    if n == '#enddefine':
                        break
                    elif n == bad_line:
                        self.error = True
                        return
                    content.append(n)
                defines[name] = list(reversed(content))
                defines_count[name] = 0
            elif line == '#enddefine':
                self.error = True
                return
            elif line.endswith(':'):
                label = line[:-1]
                if len(label.split()) != 1:
                    self.error = True
                    return
                if label in self._labels:
                    self.error = True
                    return
                self._labels[label] = len(self.code)
            else:
                cmd, *args = line.split()
                if cmd == 'push' and len(args) == 1:
                    arg = args[0]
                    if not check(arg):
                        self.error = True
                        return
                    self.code.append(('push', arg, None))
                elif cmd == 'pop' and len(args) == 1:
                    arg = args[0]
                    if arg not in self.registers:
                        self.error = True
                        return
                    self.code.append(('pop', arg, None))
                elif cmd == 'add' and len(args) == 2:
                    if args[0] not in self.registers or not check(args[1]):
                        self.error = True
                        return
                    a, b = args
                    self.code.append(('add', a, b))
                elif cmd == 'sub' and len(args) == 2:
                    if args[0] not in self.registers or not check(args[1]):
                        self.error = True
                        return
                    a, b = args
                    self.code.append(('sub', a, b))
                elif cmd == 'je' and len(args) == 2:
                    arg, label = args
                    if not (label[0] == label[-1] == '"'):
                        self.error = True
                        return
                    label = label[1:-1]
                    if not check(arg):
                        self.error = True
                        return
                    used_labels.add(label)
                    self.code.append(('je', arg, label))
                elif cmd == 'jl' and len(args) == 2:
                    arg, label = args
                    if not (label[0] == label[-1] == '"'):
                        self.error = True
                        return
                    label = label[1:-1]
                    if not check(arg):
                        self.error = True
                        return
                    used_labels.add(label)
                    self.code.append(('jl', arg, label))
                else:
                    self.error = True
                    return
        for label in used_labels:
            if not label in self._labels:
                self.error = True
                return


if __name__ == '__main__':
    import sys
    code = sys.stdin.read()
    vm = VM(code)
    if vm.error:
        print('Error while compiling code', file=sys.stderr)
        sys.exit(1)
    vm.stack = [int(arg) for arg in sys.argv[1:]]
    vm.run(0)
    if vm.error:
        print('Error while executing', file=sys.stderr)
        sys.exit(2)
    n = len(vm.stack)
    for i, v in enumerate(vm.stack):
        print(v, f'({n - i})')
