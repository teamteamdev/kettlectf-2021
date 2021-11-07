ram_size = 128

mem = [0] * ram_size

code = [int(v) for v in input().split()]

sp = ram_size - 1
mem[0] = len(code)

for ip, v in enumerate(code, 1):
    if v == 7:
        mem[sp] = ip
        sp -= 1
    elif v == 8:
        sp += 1
        opened = mem[sp]
        mem[sp] = 0
        mem[opened] = -ip
        v = -opened
    mem[ip] = v

mp = len(code) + 1
ip = 1

while mem[ip] != 0:
    cmd = mem[ip]
    if cmd == 1:
        mp -= 1
    elif cmd == 2:
        mp += 1
    elif cmd == 3:
        mem[mp] += 1
    elif cmd == 4:
        mem[mp] -= 1
    elif cmd == 5:
        print(mem[mp], end=' ')
    elif cmd == 6:
        mem[mp] = int(input())
    else:
        addr = -cmd
        if (mem[mp] == 0) == (addr > ip):
            ip = addr
    ip += 1
