from md5 import *
from pwn import *
from binascii import hexlify
# p = process(['python3','chall.py'])
p = remote('localhost', 9999)
green =xor(hash(b'green'), hash(b'1'))
red = xor(hash(b'red'), hash(b'1'))
blue = xor(hash(b'blue'), hash(b'1'))

def warmup():
    p.sendline(hexlify(blue))
    p.sendline(hexlify(green))
    p.sendline(hexlify(red))
    p.sendline(hexlify(red))
    p.sendline(hexlify(red))
    p.sendline(hexlify(red))
    p.sendline(hexlify(blue))
    p.sendline(hexlify(blue))
    p.sendline(hexlify(b"1"))
    p.sendline(hexlify(b"1"))

def real():
    p.sendline(hexlify(red))
    p.sendline(hexlify(red))
    p.sendline(hexlify(green))
    p.sendline(hexlify(green))
    p.sendline(hexlify(blue))
    p.sendline(hexlify(blue))
    p.sendline(hexlify(red))
    p.recvuntil(b"Verifier selected edge:")
    chosen_vertex = p.recvline().decode().strip()
    if ("(1, 2)" in chosen_vertex):
        p.sendline(hexlify(b"1"))
        p.sendline(b"1a17ab80ab6af088882cec5a2770ac5d") # hasil dari crack_hash.py
    elif ("(5, 6)" in chosen_vertex):
        p.sendline(hexlify(b"1"))
        p.sendline(b"eb783c44ff01200475f1d342fea39642") # hasil dari crack_hash.py
    elif ("(3, 4)" in chosen_vertex):
        p.sendline(hexlify(b"1"))
        p.sendline(b"1a17ab80ab6af088882cec5a2770ac5d") # hasil dari crack_hash.py
    else:
        p.sendline(hexlify(b"1"))
        p.sendline(hexlify(b"1"))


if __name__ == "__main__":
    try:
        for i in range(30):
            warmup()
        
        p.recvuntil(b"Now for the real challenge...")
        for i in range(100):
            real()
        p.recvuntil(b"Alright, it seems that you can be trusted. Here's the secret: \n")
        print(p.recvline().strip().decode())
    except:
        p.interactive()


    
    




