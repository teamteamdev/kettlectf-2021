def decode(flag):
    return int.to_bytes(flag, 25, "big").replace(b"\x00", b"").decode()
