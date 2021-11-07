from requests import session
s = session()
data = s.get("https://rsa_basics.team-5.school.teamteam.dev/encryption").json()
for _ in range(10):
    e = data["e"]
    m = data["m"]
    n = data["n"]
    answer = pow(m, e, n)  # Решить можно только этой функцией, так как числа достаточно большие
    data = s.post("https://rsa_basics.team-5.school.teamteam.dev/encryption", json={"answer": answer}).json()
print(data)