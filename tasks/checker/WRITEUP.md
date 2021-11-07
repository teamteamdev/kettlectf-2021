# Flag checker: Write-up

Нам дают скомпилированный байт-код Python, попробуем его запустить. Если вам не
повезет, то у вас будет ошибка наподобие Bad Magic Number. В таком случае можно
попробовать использовать `file`, но и она ничего не дает. Возможно, это довольно
свежая версия языка. Качаем, как-нибудь запускаем (`docker run -it --rm -v
$(pwd):/app python:3.10`) и радуемся.

Когда мы запустили программу она что-то ожидает на ввод, после печатает, что это
неверный флаг (либо вы очень везучий и смогли сразу ввести флаг). Попробуем
понять, что же она делает.

Если сделать `import flag_checker`, то у нас внезапно завершается процесс.
Видимо, так просто нельзя. Попробуем запустить с ключом `-i` и посмотреть на то,
что осталось через `dir()`. Видим много разных переменных, но большинство из них
(с самыми интересными названиями) содержит `None`. Придется дисассемблировать.

Пользуясь трюком со
[StackOverflow](https://stackoverflow.com/questions/59431770/why-cant-python-dis-module-disassembly-this-pyc-file)
получаем диссасемблированный байт-код. Просматривая быстрым взглядом видим
большую константу `inner` и переменную `decoded`. А в конце программы (35
строка) у нас есть вызов `exec` с кодом, очень похожим на тот, что мы уже
применяли, чтобы получить code-object. Получается, этот код как-то преобразует
`inner` в `decoded` и исполняет полученный код. Какое счастье, что у нас есть
весь байт-код. Давайте его перепишем.

```python
alphabet = b'd\xd1\x8da\xd0\xb4b\xd0\xb8e\xd1\x84'
alphabet = alphabet.decode()

decoded = []

for i in range(0, len(inner), 8):
    chunk = inner[i:i+8]
    chunk = [alphabet.index(c) for c in chunk]
    a = (chunk[0] << 5) + (chunk[1] << 2) + (chunk[2] >> 1)
    if len(chunk) == 3:
        decoded.append(a)
        break
    b = ((chunk[2] & 1) << 7) + (chunk[3] << 4) + (chunk[4] << 1) + (chunk[5] >> 2)
    if len(chunk) == 6:
        decoded.append(a)
        decoded.append(b)
        break
    c = ((chunk[5] & 3) << 6) + (chunk[6] << 3) + chunk[7]
    decoded.append(a)
    decoded.append(b)
    decoded.append(c)

for i in range(0, len(decoded), 2):
    decoded[i], decoded[i + 1] = decoded[i + 1], decoded[i]

decoded = bytes(decoded)
```

> На самом деле это реализация base8 с кастомным алфавитом и без паддинга

Получим `decoded`, сохраним его в файл и попробуем запустить. Поведение
программы не изменилось, значит мы ничего не сломали, но обошли один уровень
защиты. Повторим действия и вновь увидим байт-код. Этот значительно проще, сразу
начнем переписывать.
```python
flag = input()
res = ""
iv = 123
### ivs = []
for letter in flag:
    iv = ((iv + 13) * 37) % 256
    iv = ((iv ^ 180) - 123) % 256
    iv = iv << 3
    iv = (iv + (iv // 256)) % 256
    ### ivs.append(iv)
    res += hex(ord(letter) ^ iv)[2:].rjust(2, '0')
if res == "66ba1d8d130d481c787e5bd4ecf34bccb019f4b0bdd48e09171e":
    print("[+] You entered a real flag!")
else:
    print("[-] This is not a real flag!")
### s = '66ba1d8d130d481c787e5bd4ecf34bccb019f4b0bdd48e09171e'
### chars = [s[i:i+2] for i in range(0, len(s), 2)]
### print(''.join(chr(i ^ c) for i, c in zip(ivs, chars)))
```

Читаем наш ввод, кодируем и сравниваем с какой-то волшебной строчкой. Видим, что
там у нас обычный xor, значит мы можем получить исходные символы флага обратным
xor. Выполняем, получаем флаг.

Флаг: **kettle\_4ma0\_b1lan\_r0ot_0ne**
