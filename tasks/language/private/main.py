
from PIL import Image, ImageDraw


def circle(i, dm, x1, y1, character):
    x2 = x1 + dm
    y2 = y1 + dm
    if character == '_':
        i.rectangle((x1, y1, x2, y2), outline='white')
    else:
        i.ellipse((x1, y1, x2, y2), outline='white')


imgsize = (16384, 16384)
img = Image.new('RGBA', imgsize, (0, 0, 0, 0))

flag = input()
x = 0
y = 0
md = 0

for symbol in flag:
    d = ord(symbol)
    if d > md:
        md = d
idraw = ImageDraw.Draw(img)
for symbol in flag:
    diameter = ord(symbol)
    y = (md - diameter) // 2
    circle(idraw, diameter, x, y, symbol)
    x += diameter // 2
r = 255
g = 0
b = 0
state = 'red'
stateb = 'white'
for x in range(x+md//2+1):
    if r > 0 and state == 'red':
        r -= 1
        g += 1
    else:
        if g > 0 and state != 'blue':
            g -= 1
            if state == 'green':
                r += 1
                if r == 255:
                    state = 'red'
            else:
                b += 1
                if b == 255:
                    state = 'blue'
        else:
            b -= 1
            g += 1
            if b == 0:
                state = 'green'
    for y in range(md+1):
        if img.getpixel((x, y)) == (255, 255, 255, 255):
            img.putpixel((x, y), (r, g, b))

del idraw

img = img.crop((0, 0, x+md//2, md+1))
img.save('heptapod_b.png')
