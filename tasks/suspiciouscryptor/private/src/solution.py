def generate_key(seed):
    key = []
    for _ in range(64):
        seed = (seed * 128 + 1337) % 127
        # не самая лучшая формула для генерации ключа
        # так как для многих сидов сгенерируется один и тот же ключ
        # не делайте так :^) 
        key.append(seed)
    return key


with open("message.txt", "rb") as f:
    message = f.read()

for seed in range(1, 10001):
    key = generate_key(seed)
    # Мы знаем, что флаг начинается с kettle_
    # Поэтому будем проверять только первые 7 байт
    # Если всё совпадёт, то это флаг
    flag_start = "kettle_"
    dec = ""
    for i in range(64):
        dec += chr(message[i] ^ key[i])
        if i <= 6 and dec[i] != flag_start[i]:
            break
    else:
        print(dec)
        break