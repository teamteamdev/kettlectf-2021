#!/usr/bin/env python3

count=0
while count!=1:
    a=str()
    c=str()
    print("Введите логин:")
    login=input()
    length=len(login)
    for i in range (0,length):
        a=ord(login[i])
        a=a+1
        a=a**2
        a=bin(a)
        a=a[2::]
        a=a[::-1]
        c=str(c)+"|"+str(a)
    a=str()
    k=str()
    print("Введите пароль:")
    password=input()
    length=len(password)
    for i in range (0,length):
        a=ord(password[i])
        a=a+2
        a=a**3
        a=bin(a)
        a=a[2::]
        a=a[::-1]
        k=str(k)+"|"+str(a)   
    if c=="|00100010111101|00000000100011|10000100000011|00100001101001|10010110011101|00100111110101|00001001001011|00100001101001|001000111001|000000100011|001001001011|000010010101|100111110101|100011010011|100010111101|100101000101|001001101101" and k=="|000110000100100010011|000101100011010001001|111011100011010100001|000111001111001000101|11011100011100110111|101100100000111000011|000110000100100010011|101100100000111000011|111001010110110110011|000100101101100101101|000100101101100101101|111011100011010100001|000000101000101111101|111001111001000101|000000101010010001|000000000111010101|000101000101111101|000110001110011001|101100011010001001|110000100100010011|100101101100101101|110101000110000001":        
        count=count+1       
        f=open('flag.txt','r',-1,'utf-8')
        for line in f:
            print(line)
        input()
    else:
        print("Неверный пароль или пароль!")
    a=str()
    k=str()
    c=str()
