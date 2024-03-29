# RSA basics: Write-up

Перед нами очень красивый сайт на котором 4 ссылки на упражнения и извещение о формате частей флага. В нём говориться, что нужно использовать какой-то метод класса `int` в Python. Речь о `int.to_bytes()` и `int.from_bytes()`.

Функция `int.to_bytes()` принимает на вход число, длину (< 25) и byteorder ("big").

Приведу функцию для декода:
```python
def decode(flag):
    return int.to_bytes(flag, 25, "big").replace(b"\x00", b"").decode()
```
## Решения упражнений

### Challenge 1
```python
from requests import session
s = session()
data = s.get("https://rsa_basics.team-5.school.teamteam.dev/encryption").json()
for _ in range(10):
    e = data["e"]
    m = data["m"]
    n = data["n"]
    answer = pow(m, e, n)  # Решить можно только этой функцией, так как числа достаточно большие
    data = s.post("https://rsa_basics.team-5.school.teamteam.dev/encryption", json={"answer": answer}).json()
print(data)
```
Получаем: `{'description': 'First part: kettle_rsa_', 'status': 'success'}`

Первая часть флага: `kettle_rsa_`

### Challenge 2
Нам даны n, e, p и c. Этих данных достаточно, чтобы восстановить приватный ключ.

```python
from decode import decode

n = ...
e = ...
p = ...
c = ...

q = n // p
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
m = pow(c, d, n)

print(decode(m))
```
Вторая часть флага: `is_not_so_hard_`

### Challenge 3
Сервис шифрует и расшифровывает сообщения, при чём p, q и e всегда одинаковые, значит и приватный ключ с публичным статичны, тогда мы можем воспользоваться мультипликативным свойством RSA (`подсказка была в адресной строке ;^)`):

`E(m1) * E(m2)= E(m1 * m2)`

Тогда

`D(E(m1) * E(m2)) = D(E(m1 * m2))`

`D(E(m1) * E(m2)) = m1 * m2`

`m1 = D(E(m1) * E(m2)) // m2`

Пусть `m1` - часть флага, `m2 = 31337`, с помощью сайта мы можем получить `E(m2) = 3828742309428451447110634493726438777890733303049569167057`

Нам дано: `E(m1) = 29862893681134883361798406196132397005733179295814546292287`

Тогда: `E(m1) * E(m2) = 114337324518924683075690975634057437713813459241967859204452192762783532975250897708188992258656167800014034253589359`

Теперь с помощью сайта получаем `D(E(m1) * E(m2)) = 4827217855767003312264487717513672916522492851604910793`

Находим `m1 = 4827217855767003312264487717513672916522492851604910793 / 31337 = 154042118127676654187206424275255222788476652251489`

Декодируем и получаем третью часть флага: `if_you_read_wikipedia`

### Challenge 4
Здесь нам необходимо расшифровать последнюю часть флага, зная только публичный ключ. Заметим, что модуль достаточно мал, значит можно попробовать восстановить p и q, а затем получить приватный ключ. Факторизовать данное число можно с помощью [factordb](http://factordb.com/).

последняя часть: `_lol`

Флаг: **kettle_rsa_is_not_so_hard_if_you_read_wikipedia_lol**
