# Крестики-нолики: Write-up

Для решения задания нужно написать схожую программу:
```
with open("ttt.txt") as file:
    f = file.readlines()
d = 'xx xxx xxx xx xx xx xxx xx xxx xx xxx xxx xxx xxx xx xxx xxx xxx xxx xx xxx xxx xxx xxx xxx xxx xxx xxx xx xxx xxx xxx xxx xx xxx xxx xxx xxx xxx xx xxx xx xxx xxx xxx xx xxx xxx xx xxx xxx xxx xx xxx xxx xx xxx xx xx xxx xx xxx xxx xxx xx xxx xxx xxx xxx xx xx xxx xxx xxx xxx xxx xx xx xx xxx xxx xx xxx xx xx xx xxx xx xxx xxx xxx xxx xx xxx xxx xx xxx xxx xxx xx xxx xx xxx xxx xxx xx xx xxx xxx xx xxx xxx xxx xxx xx xxx xxx xx xxx xxx xxx xxx xx xxx xxx xx xxx xx xx xxx xxx xxx xxx xxx xxx xx xx xxx xxx xxx xxx xx xxx xxx xx xx xxx xxx xxx xxx xxx xx xx xx'
def func():
    c = []
    for i in range(0, 2466, 6):
        a = f[1+i] + f[2+i] + f[3+i]
        a = a[0] + a[3] + a[6] + a[10] + a[13] + a[16] + a[20] + a[23] + a[26]
        if a[0] == '2' and ((a[1] == '1' and a[2] == '1') or (a[6] == '1' and a[3] == '1') or (a[4] == '1' and a[8] == '1')):
            c.append('1')
        elif a[1] == '2' and ((a[2] == '1' and a[0] == '1') or (a[7] == '1' and a[4] == '1')):
            c.append('2')
        elif a[2] == '2' and ((a[0] == '1' and a[1] == '1') or (a[8] == '1' and a[5] == '1') or (a[6] == '1' and a[4] == '1')):
            c.append('3')
        elif a[3] == '2' and ((a[4] == '1' and a[5] == '1') or (a[6] == '1' and a[0] == '1')):
            c.append('4')
        elif a[4] == '2' and ((a[5] == '1' and a[3] == '1') or (a[7] == '1' and a[1] == '1') or (a[8] == '1' and a[0] == '1') or (a[6] == '1' and a[2] == '1')):
            c.append('5')
        elif a[5] == '2' and ((a[3] == '1' and a[4] == '1') or (a[8] == '1' and a[2] == '1')):
            c.append('6')
        elif a[6] == '2' and ((a[7] == '1' and a[8] == '1') or (a[0] == '1' and a[3] == '1') or (a[4] == '1' and a[2] == '1')):
            c.append('7')
        elif a[7] == '2' and ((a[8] == '1' and a[6] == '1') or (a[1] == '1' and a[4] == '1')):
            c.append('8')
        elif a[8] == '2' and ((a[0] == '1' and a[4] == '1') or (a[2] == '1' and a[5] == '1') or(a[6] == '1' and a[7] == '1')):
            c.append('9')
        else:
            c.append('0')
    j = 0
    g = []
    for i in range(len(d)):
        if d[i] == 'x':
            g.append(c[i-j])
        else:
            g.append(' ')
            j += 1
    l = ''
    for i in range(len(g)):
        l = l+g[i]
    print(l)
func()
```
Полученный набор чисел нужно декодировать из ASCII в текст при помощи информации данной в описании

Флаг: **kettle_chess_is_better_63**
