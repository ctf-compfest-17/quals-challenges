from md5 import *
from pwn import xor
from binascii import hexlify, unhexlify
def test():
    red = hash(b"green")
    key = hash(b"1")
    green = hash(b"red")
    secret = xor(red, key)
    cracked = xor(secret, green)
    print("Cracked:",hexlify(cracked))
    key2 = hash(unhexlify("1a17ab80ab6af088882cec5a2770ac5d"))
    assert xor(green, key2) == xor(red, key)

if __name__ == "__main__":
    test()