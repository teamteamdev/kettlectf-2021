import pwn
fin = open("flag.enc","rb")
fl = fin.read()
fin.close()
i = 0
arr = []
arr2 = []
for bt in range(256):
	bt1 = ((bt * pow(3,-1,256)) % 256) ^ 123
	bt1 = (((bt1 - 7) % 256) * pow(17,-1,256)) % 256
	arr.append(bt1)
	arr2.append(pwn.p8(bt))
print("arr")
fout = open("flag2.png", "wb")
r = 0
for bt in fl:
	fout.write(arr2[arr[bt]^i])
	i = bt
	r += 1
	if r == 1024:
		r = 0
		i = 0
fout.close()
print("done")
