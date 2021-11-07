from hashlib import sha256

with open("hash", "r") as f:
    flag_hash = f.read()

with open('list_of_birds.txt', 'r', encoding='utf-8') as f:
    birds = f.readlines()

for bird1 in birds:
    bird1 = bird1.strip()
    for bird2 in birds:
        bird2 = bird2.strip()
        for i in range(1, 256):
            PASS = f"kettle_{bird1}_abu_1337_pr0g3r_{bird2}_{hex(i)[2:].rjust(2, '0')}"
            if sha256(PASS.encode()).hexdigest() == flag_hash:
                print(PASS)
                exit()