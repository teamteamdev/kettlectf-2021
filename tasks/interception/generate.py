from Crypto.Util import number
import os
import pyAesCrypt

file = "flag.txt"

def random_number(b):
	prime_number = number.getPrime(b)
	print(prime_number)

def diffie_hellman():
	p,g = 302304118860350364158943550303980866023,226979527512731406701562925711004201567
	a = 324248463877782095453964001151498939063
	b = 236003563297020237938193631849667525989

	A = pow(g,a,p)
	B = pow(g,b,p)

	client_private_key = pow(B,a,p)

	server_private_key = pow(A,b,p)

	print(A,B)
	print(client_private_key,server_private_key)

def crypt(file):
    key = input('Enter key: ') 
    bufferSize = 512*1024 
    pyAesCrypt.encryptFile(file,file+'.aes',key, bufferSize)
    print('[Crypted] '+file+'.aes')

def decrypt(file):
	key = input('Enter key: ') 
	bufferSize = 512*1024
	pyAesCrypt.decryptFile(file+'.aes',"kettle_flag.txt",key,bufferSize)