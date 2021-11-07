# mirror up-down left-right: Write-up

Дан непонятный файл, в котором, однако, явно виден hexdump. Кидаем в cyber chef, и нажимаем волшебную палочку:

![cyber](src/imgs/chef.jpg)

1) Видим очень много строчек, в каждой из которых по три элемента, зашифрованных явно в base64.
2) Если посмотреть на название и подсказки, то можно догадаться, что это список пикселей(r, g, b).
   Поэтому пишем программу с помощью Python и библиотеки PIL например, которая создаёт картинку по данным значениям.
```python
from PIL import Image
import base64


def create_image(file, width, height):
    im = Image.new("RGB", (width, height))
    pix = im.load()
    with open(file, 'r') as f:
        gg = f.readlines()
    x, y = im.size
    for i in range(x):
        for j in range(y):
            row = gg[j + i * 34].strip().split()
            r = base64.b64decode(row[0].encode('ascii')).decode('ascii')
            g = base64.b64decode(row[1].encode('ascii')).decode('ascii')
            b = base64.b64decode(row[2].encode('ascii')).decode('ascii')
            pix[i, j] = int(r), int(g), int(b)
    im.save('your_image_name.png')


create_image('your_file_name.txt', 712, 34)
```
На выходе получаем вот такое изображение:

![odd](src/imgs/try.png)

3) Вспоминаем название, которое является инструкцией - отзеркалить картинку и затем поменять местами верх, низ, правую часть, левую часть. Опять же, легче написать небольшой код:

```python
from PIL import Image


def mirror():
    im = Image.open('your_image_name.png')
    pixels = im.load()
    x, y = im.size
    for i in range(x // 2):
        for j in range(y):
            pixels[i, j], pixels[x - i - 1, j] = pixels[x - i - 1, j], pixels[i, j]
    im.save('your_image_name1.png')


mirror()
```
зеркало

```python
from PIL import Image


def twist_image(inp_name, out_name):
    im = Image.open(inp_name)
    x, y = im.size
    im1 = im.crop((0, 0, x, y // 2))
    im2 = im.crop((0, y // 2, x, y))
    im.paste(im2, (0, 0))
    im.paste(im1, (0, y // 2))
    im1 = im.crop((0, 0, x // 2, y))
    im2 = im.crop((x // 2, 0, x, y))
    im.paste(im2, (0, 0))
    im.paste(im1, (x // 2, 0))
    im.save(out_name)


twist_image('your_image_name1.png', 'your_image_name2.png')
```
up-down left-right

4) Получили картинку с ссылкой:

![ref](src/imgs/ref.png)

5) Переходим и попадаем на видео с сомнительным содержимым, однако спускаемся в описание и видим:

![flag](src/imgs/answer.jpg)

6) В начале описания есть словосочетание <b>exclusive or</b>, которое означает <b>исключающее или</b> или попросту XOR. Заходим в любимый **cyber chef** и через XOR brute force находим флаг:

![answer](src/imgs/flag.jpg)

Флаг: **kettle_you_are_so_persistent**
