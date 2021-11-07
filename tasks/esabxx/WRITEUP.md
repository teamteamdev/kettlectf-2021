# esabXX: Write-up

> 13кзытт3мыно22аъ5хущшюв

Смотрим на строчку, видим циферки и буквы кириллицы. Берем русский алфавит,
добавляем его к `0123456789` и получаем новые цифры в некой системе счисления.

```python
def parse(num, base):
    alph = '01234...'  # digits + russian letters
    res = 0
    for i, c in enumerate(reversed(num)):
        res += alph.index(c) * base ** i
    return res
```

С помощью этого кода мы можем перевести число в привычный вид. Далее разобьем
число на байты и будем считать каждый буквой.

```python
def split_num(num):
    chars = []
    while num:
        chars.append(num & 255)  # last byte
        num >>= 8
    return ''.join(chr(c) for c in chars[::-1])
```

После этого перебираем все возможные `base` от двух до 43 (размер алфавита) и пытаемся найти то, которое после расшифровки будет начинаться на `kettle_`. Таким будет только основание 42.

Флаг: **kettle\_loves\_42**
