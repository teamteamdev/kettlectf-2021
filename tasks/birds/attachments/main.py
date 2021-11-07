from random import choice

with open("list_of_birds.txt", "r", encoding="utf-8") as f:
    birds = f.readlines()
    bird1 = choice(birds).strip()
    bird2 = choice(birds).strip()
password = f"kettle_{bird1}_abu_1337_pr0g3r_{bird2}_{hex(choice(range(1, 256)))[2:].rjust(2, '0')}"
print(password)