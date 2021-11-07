# ЕГЭ по физике: Write-up

Цель задания решить 130 заданий из ЕГЭ по физике и вписать сумму всех ответов в отаедённое для этого поле.

Первым делом можно перейти в источник указаный на страницке с заданием(https://phys-ege.sdamgia.ru) и открыть любое задание. После чего посмотреть как выглядит его url:
![url задания](writeup/url.png)


 Дальше делаем get запрос на страницу таска:
```python
 import requests
 
 r = requests.get('https://physicsege.board.kettlec.tf/')
 t = r.text
 print(t)
```
 При анализе ответа можно заметить что все id заданий идут после class="s4">
 
 
 Найдём id первого задания и составим его url:
```python
 import requests
 
 r = requests.get('https://physicsege.board.kettlec.tf/')
 t = r.text
 
 url = 'https://phys-ege.sdamgia.ru/problem?id='
 
 x = t.find('class="s4">')
 id = (t[x+11:x+16])

fullurl = url + id
```
 
 Теперь можем найти ответ, он идёт после 'Ответ:</span>'(тут не отображается, но в коде можешь посмотреть после чего):
```python
import requests
 
r = requests.get('https://physicsege.board.kettlec.tf/')
t = r.text
 
url = 'https://phys-ege.sdamgia.ru/problem?id='
 
x = t.find('class="s4">')
id = (t[x+11:x+16])

fullurl = url + id

r2 = requests.get(fullurl)
t2 = r2.text
y = t2.find('Ответ:</span>')
answer = (t2[y+14:y+17])
print(answer)
```
 
 Осталось написать цикл и создать условия при которых наличее в id и answer лишьних символов сокращает их длину. И вот готовый код:
```python
import requests
 
r = requests.get('https://physicsege.board.kettlec.tf/')
t = r.text
fullanswer = 0
 
url = 'https://phys-ege.sdamgia.ru/problem?id='
for i in range(130):
    x = t.find('class="s4">')
    id = (t[x+11:x+16])
    if '<' in id:
        id = (t[x+11:x+15])

    fullurl = url + id

    r2 = requests.get(fullurl)
    t2 = r2.text
    y = t2.rfind('Ответ:</span>')
    answer = (t2[y+14:y+17])
    if '.' in answer:
        answer = t2[y+14:y+16]
    if '<' in answer:
        answer = t2[y+14:y+16]
    fullanswer = fullanswer + int(answer) 
    t = t[x+12:]
    
print(fullanswer)
```

Полученный ответ вводим в форму и получаем флаг.

Флаг: **kettle_you_are_god_damn_right_b64acdbkjs78hw7ed**
