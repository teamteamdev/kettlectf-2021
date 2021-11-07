import math

a = int(input())
b = int(input())
c = int(input())

if a == b == 0:
    print('none' if c else 'inf')
elif a == 0:
    x = -c // b
    print(x)
else:
    d = b**2 - 4 * a * c
    if d < 0:
        print('none')
    elif math.isclose(d, 0):
        x = -b // (2 * a)
        print(x)
    else:
        d = round(math.sqrt(d))
        x1 = (-b - d) // (2 * a)
        x2 = (-b + d) // (2 * a)
        print(x1, x2)
