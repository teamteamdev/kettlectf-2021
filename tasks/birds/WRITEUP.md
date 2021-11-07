# Птички: Write-up

1. Скачиваем файлы `hash.txt` и `main.py`

2. По скрипту, который генерирует пароль, видно, что открывается файл на чтение с названием `list_of_birds.txt`.
Ищем его и скачиваем по первой же [ссылке](https://gist.githubusercontent.com/jason-kane/a12aba88f84cf84906344f5fac6b33b7/raw/254be1138841f3936ffc25388381070d6bf341b1/list_of_birds.txt).

1. Добавим `list_of_birs.txt` в одну директорию со скриптом и дополним скрипт, перебирающий все возможные пароли:

```python
from hashlib import sha256

with open("hash", "r") as f:
    flag_hash = f.read()

with open('list_of_birds.txt', 'r', encoding='utf-8') as f:
    birds = f.readlines()

for bird1 in birds:
    bird1 = bird1.strip()
    for bird2 in birds:
        bird2 = bird2.strip()
        for i in range(1, 256):
            PASS = f"kettle_{bird1}_abu_1337_pr0g3r_{bird2}_{hex(i)[2:].rjust(2, '0')}"
            if sha256(PASS.encode()).hexdigest() == flag_hash:
                print(PASS)
                exit()
```

4. Запускаем программу и получаем флаг.

Флаг: **kettle_mousebird_abu_1337_pr0g3r_618**
