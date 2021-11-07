# Вредоносные программы: Write-up

Читаем описание таска. Ниже видим ссылку. Если перейти по этой ссылке, мы попадем в телеграм канал. Изучаем этот канал и находим ссылку на репозиторий github. На github куча бесполезной информации, странные коды на python и т.д. Еще там есть интересный файл с названием "email.txt". В нем написаны почты покупателей, а так же дата покупки. Перечитаем легенду таска. Там написано: "Он узнал, что вчера этот человек приобрел какую-то программу...". Смотрим какое число было вчера. Вчера было 27 октября. Нажмем CTRL+F и поищем "27.10.2021". Этот поиск находит очень странную почту "anonimus42@mailforscam.site". Пробуем перейти по адресу "mailforscam.site" и нас встречает форма входа. Вводим наш адрес "anonimus42" и видим два письма. Первое письмо указывает нам, что искомая нами информация находится во втором письме. Второе письмо от ФСБ и в нем нет ничего полезного. Обратим внимание по каким адресам находятся письма. Письмо с чеком: "check-email/1". Письмо от ФСБ: "check-email/3". Похоже письмо №2 куда-то пропало. Пробуем обратиться на подобный адрес, где вместо 1 и 3 будет 2: "check-email/2" и находим наше пропавшее письмо, в котором кодом активации является флаг.

Флаг: **kettle_viruses_are_bad_56k31gg9j3**