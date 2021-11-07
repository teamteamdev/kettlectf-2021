if __name__ != '__main__':
    import sys
    sys.exit(0)
else:
    flag = input()
    res = ""
    iv = 123
    for letter in flag:
        iv = ((iv + 13) * 37) % 256
        iv = ((iv ^ 180) - 123) % 256
        iv = iv << 3
        iv = (iv + (iv // 256)) % 256
        res += hex(ord(letter) ^ iv)[2:].rjust(2, '0')
    if res == "66ba1d8d130d481c787e5bd4ecf34bccb019f4b0bdd48e09171e":
        print("[+] You entered a real flag!")
    else:
        print("[-] This is not a real flag!")
    flag = None
    iv = None
    res = None
