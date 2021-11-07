import telebot
import config
from telebot import types
import random
import time

bot = telebot.TeleBot(config.TOKEN)
funny_stories = ['Что делает Ельцин когда у него кончаются сигареты? Стреляет парламент.',
                 'Заходит черепаха в бар и заказывает стакан воды. На следующий день она снова заходит и заказывает стакан. На третий день такая же ситуация. Так продолжалось всю неделю. На седьмой день бармен спрашивает у черепахи: У нас столько алкоголя, зачем ты воду берешь? Черепаха отвечает: У меня дом горит.',
                 'Приходит один программист другому: — Слышь, Петя, мне генератор случайных чисел нужен. — Четырнадцать!',
                 'Программиста спрашивают: '
                 '— Скажите, который час?'
                 '— «Который час», если Вас это прикалывает.',
                 "— Как отличить наркомана от программиста? — Задать контрольный вопрос — что для вас значит фраза:  — Отдай винт, а то я твою маму продам?",
                 'Программист вбегает в полицию: — У меня автомобиль пропал! — Опять вы! Да не пропал он никуда, стоит где оставили... Запомните, 404 — это его госномер!!!',
                 'Опытный разработчик всегда посмотрит направо и налево, даже если переходит улицу с односторонним движением.',
                 'Зачем нужно плохое ПО? Без него у многих программистов не будет работы.',
                 'Основные изменения в новой версии программы: исправлены старые баги, добавлены новые.',
                 'Программирование состоит на 10% из строгой науки, на 20% из смекалки и вдохновения, и на 70% из попыток совместить первое со вторым.',
                 'Не помещаются мысли в голове? Воспользуйтесь архиватором!',
                 'Цыгани украли моего отца, золотой был человек.'
                 ]


def is_digitalpha(text):
    text = list(text)
    flags = [False, False]
    for i in text:
        if i.isdigit():
            flags[0] = True
        elif not i.isdigit():
            flags[1] = True

    if flags[0] == True and flags[1] == True:
        return True
    else:
        return False


def is_digit(text):
    try:
        text = int(text)
        return True
    except Exception:
        return False


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='🥶Анекдоты🥶',
                                         callback_data='funny stories')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🥶Анекдоты🥶')
    keyboard.add(item1)
    markup.add(button1)
    bot.send_message(message.chat.id,
                     'Бот разработанный для команды Bad Request, носит развлекательный характер. Пока что он умеет читать только анекдоты, ждите новых обновлений!',
                     reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def reply_message(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('☑️', callback_data='correct')
    item2 = types.InlineKeyboardButton('❌', callback_data='incorrect')
    markup.add(item1, item2)

    if message.text == '🥶Анекдоты🥶':
        bot.send_message(message.chat.id, 'Для получения анекдота подтвердите возраст, вам больше 18 лет?',
                         reply_markup=markup)
        bot.register_next_step_handler(message, age_validate)

    elif message.text == 'Анекдоты' or message.text == 'анекдоты':
        bot.send_message(message.chat.id, '''Traceback (most recent call last):
  File "<input>", line 1, in <module>
NameError: name 'by_friends_of_petya_' is not defined
''')
        time.sleep(2)
        bot.send_message(message.chat.id, '☠Мы испытываем технические неполадки☠')
    else:
        bot.send_message(message.chat.id, 'Я вас не понимаю😢')


@bot.message_handler(content_types=['photo'])
def return_flag(message):
    try:
        if message.content_type == 'photo':
            bot.send_message(message.chat.id, '''Traceback (most recent call last):
  File "<input>", line 1, in <module>
NameError: name '5ef1jb81a' is not defined
''')
            time.sleep(2)
            bot.send_message(message.chat.id, '☠Мы испытываем технические неполадки☠')

    except Exception:
        print(Exception)


def request_flag(message):
    try:
        if message.text.isalpha():
            bot.send_message(message.chat.id, '{} остаётся без флага'.format(message.text))
        else:
            bot.send_message(message.chat.id, ']>§öZq¿')
            time.sleep(2)
            bot.send_message(message.chat.id, '☠Мы испытываем технические неполадки☠')
            time.sleep(2)
            bot.send_message(message.chat.id, 'flag')
    except Exception:
        print(Exception)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'funny stories':
                bot.register_next_step_handler(call.message.text, age_validate)
            elif call.data == 'correct':
                bot.send_message(call.message.chat.id, ''.join(random.choice(funny_stories)))
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            elif call.data == 'incorrect':
                bot.send_message(call.message.chat.id, 'Вы слишком юны, возвращайтесь как подрастёте')
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


    except Exception:
        print(Exception)


def age_validate(message):


    if message.content_type != 'photo':
        if message.text == '🥶Анекдоты🥶' or message.text == 'анекдоты' or message.text == 'Анекдоты':
                print('done')
                reply_message(message)
        else:
            time.sleep(2)
            bot.send_message(message.chat.id, '''Traceback (most recent call last):
      File "\psf\Home\Documents\copy_folder.py", line 4, in <module>
        shutil.copytree(src, dst_sav)
      File "C:\Python39\lib\kettle_problem_bot_", line 177, in copytree
        os.makedirs(dst)
      File "C:\Python39\lib\os.py", line 157, in makedirs
        mkdir(name, mode)''')
            time.sleep(2)
            bot.send_message(message.chat.id, '☠Мы испытываем технические неполадки☠')
    else:
        bot.send_message(message.chat.id, '''Traceback (most recent call last):
          File "<input>", line 1, in <module>
        NameError: name '5ef1jb81a' is not defined
        ''')
        time.sleep(2)
        bot.send_message(message.chat.id, '☠Мы испытываем технические неполадки☠')


if __name__ == '__main__':
    bot.infinity_polling()
