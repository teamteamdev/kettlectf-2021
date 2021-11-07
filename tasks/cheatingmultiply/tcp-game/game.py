#!/usr/bin/env python3

import random
print('Игра "Преумножь капитал"')
print('Вам будет дан стартовый капитал в размере 1000 валюты')
print('Вы сможете указать размер своей ставки')
print('Угадайте число загаданное компьютером')
print('Это число от 1 до 10')
print('У вас будет только 10 попыток')
print('Если угадаете за указанное количество попыток, то ваша ставка удвоится')
print('Игра будет продолжаться до тех пор пока вы не достигните 1000000')
print('Если вы набрали миллион, то вы выиграли!!!')
print()

wallet = 1000
while True:
    opinion = input('Вы готовы? y/n: ')
    if opinion == 'y':
        dup = wallet
        print('Ваш капитал:', dup)
        spent = int(input('Сделайте ставку: '))
        while spent > dup:
            print('Ваш капитал:', dup)
            print('У вас не хватает денег !!!')
            print()
            spent = int(input('Сделайте ставку: '))
    if opinion == 'n':
        break
    print()
    print('Игра началась!')
    for i in range(10):
        guess = int(input('Угадывайте число: '))
        x = random.randint(1, 10)
        print('Компьютер загадал: ', x)
        print('Вы ввели: ', guess)

        if x == guess:
            wallet += 2 * spent
            print('Вы угадали!!! Ваш капитал увеличен')
            if wallet >= 1000000:
                wallet = 999999
            print('Текущий капитал', wallet)
            print()
            break

    else:
        wallet = wallet - spent
        print('Вы проиграли!!! Ваш капитал уменьшен, попробуйте еще раз')
        print('Текущий капитал', wallet)

        if wallet > 1000000:
            print('Вы определенно удачливый человек!!! Отличная работа')
            print('Вот флаг: kettle_typical_it_earnings_be_like')
            break

        if wallet == 0:
            wallet = 1000