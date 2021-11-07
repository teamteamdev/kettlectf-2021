# Quad Fkc?: Write-up

> Сначала прочитайте write-up к заданию [qasm](../qasm/WRITEUP.md)

На сей раз нам дали чуть более сложную задачу, но и дали чуть больше
возможностей -- теперь у нас есть random access memory. Как и прежде, сначала
полезно написать реализацию на чем-то более высоком
([solution.py](writeup/solution.py))
```python
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
```

Идея простая: будет записывать все команды в оперативную память, но вместо
команд перехода будем записывать адрес, который вычисляем на этапе компиялции
через стек. А после заводим instruction pointer and memory pointer и аккуратно
исполняем код.

Память мы разделяем на две части: код (начиная с адреса 1) и сами данные, между
которыми один ноль. Поскольку у нас все адреса не меньше 1, а команды целые
положительные числа или отрицательные адреса (меньше нуля), то мы сможем
определить конец, когда IP будет указывать на ноль.

> Код довольно медленный, а числа на ленте бесконечные в обе стороны, поэтому нельзя считать это полноценный BF

Затем просто аккуратно переносим это в машину Васи и радуемся тому, что у нас все работает: [solution](writeup/solution).

Флаг: **kettle\_va39a\_is\_sm8rt_b0y**
