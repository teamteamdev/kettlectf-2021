# Петин бот: Write-up


В задании нам дана лишь ссылка на телеграм бота,
перейдя по которой мы увидим собственного самого бота.

![img.png](WRITEUP/img.png)

Нажав на кнопку старт мы увидим, что бот встречает нас
приветственным письмом и предложением получить анекдот,
нажав кнопку `🥶Анекдоты🥶`.

![img_11.png](WRITEUP/img_11.png)

Нажав на неё, бот попросит пройти проверку на возраст.

![img_12.png](WRITEUP/img_12.png)

Если ввести неожидаемый ввод для бота, а именно любые символы вместо нажатия кнопок, он выдаст часть флага
`kettle_problem_bot_`.

![img_13.png](WRITEUP/img_13.png)

Также можно заметить, что бот исключительно текстовый и если попробовать отправить ему фото, 
бот выпадет в ошибку и отдаст ещё одну часть флага `5ef1jb81a` .

![img_14.png](WRITEUP/img_14.png)

Также если заметить, что мы всегда взаимодействуем с ботом, искючительно через кнопки, можно попробовать написать
`анекдоты` самостоятельно. Тогда это вновь вызовет ошибку у бота и мы получим последнюю часть флага `by_friends_of_petya_`.

![img_1.png](WRITEUP/img_1.png)

Логически соединив все части во едино, мы получим флаг.

Флаг: **kettle_problem_bot_by_friends_of_petya_5ef1jb81a**