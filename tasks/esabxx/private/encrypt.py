from functools import reduce

def convert(num: int, base: int) -> list[int]:
    if num == 0:
        return [0]
    digits = []
    while num > 0:
        num, d = divmod(num, base)
        digits.append(d)
    return digits[::-1]

flag = input()
num = reduce(lambda r, c: (r << 8) + c, (ord(c) for c in flag))
alphabet = '0123456789абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

encoded = convert(num, 42)

print(*(alphabet[i] for i in encoded), sep='')
