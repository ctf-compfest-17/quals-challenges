

p = 4079919672758639624917
a = 132047653857099716108
b = 96180839960861758201

from md5 import *
from pwn import *
from binascii import hexlify
#proc = process(['python3','chall.py'])
proc = remote('localhost', 9999)
green =xor(hash(b'green'), hash(b'1'))
red = xor(hash(b'red'), hash(b'1'))
blue = xor(hash(b'blue'), hash(b'1'))
out = []
def warmup():
    graph = {
        0:"(1, 2)",
        1: "(1, 3)",
        2: "(1, 4)",
        3: "(1, 5)",
        4: "(1, 6)",
        5: "(2, 3)",
        6: "(2, 4)",
        7: "(2, 5)",
        8: "(2, 6)",
        9: "(3, 7)",
        10: "(3, 8)",
        11: "(4, 7)",
        12: "(4, 8)",
        13: "(5, 7)",
        14: "(5, 8)",
        15: "(6, 7)"
    }
    proc.sendline(hexlify(blue))
    proc.sendline(hexlify(green))
    proc.sendline(hexlify(red))
    proc.sendline(hexlify(red))
    proc.sendline(hexlify(red))
    proc.sendline(hexlify(red))
    proc.sendline(hexlify(blue))
    proc.sendline(hexlify(blue))
    proc.recvuntil(b"Verifier selected edge:")
    chosen_edge = proc.recvline().decode().strip()
    key = list(graph.keys())[list(graph.values()).index(chosen_edge)]
    out.append(key)
    proc.sendline(hexlify(b"1"))
    proc.sendline(hexlify(b"1"))

def lcg(s, a, b, p):
    return (a * s + b) % p
def get_roll():
    global seed2
    seed2 = lcg(seed2, a, b, p)
    return seed2 % 16

def real(crack):
    graph = {
        0: (1, 2),
        1: (1, 3),
        2: (1, 4),
        3: (1, 5),
        4: (2, 3),
        5: (2, 4),
        6: (2, 5),
        7: (3, 4),
        8: (3, 5),
        9: (4, 5),
        10: (1, 6),
        11: (2, 6),
        12: (3, 6),
        13: (4, 6),
        14: (5, 6),
        15: (6, 7)
    }
    edge = graph[crack]
    for i in range(7):
        if i+1 == edge[0]:
            proc.sendline(hexlify(red))
        elif i+1 == edge[1]:
            proc.sendline(hexlify(blue))
        else:
            proc.sendline(b"12345678901234567890123456789012".hex()) # we dont care
    
    proc.sendline(hexlify(b"1"))
    proc.sendline(hexlify(b"1"))


if __name__ == "__main__":
    proc.sendline(b"1")
    for i in range(30):
        warmup()

    l = out
    n = len(out)
    A = [[0 for _ in range(n+1)] for _ in range(n+1)]
    inv100 = pow(16,-1,p)
    for i in range(n-1):
        A[i][i] = p
        A[n-1][i] = a**(i+1)%p
        A[n][i] = (a*l[0]+b-l[1])*inv100%p if i==0 else (a*A[n][i-1] + (a*l[i]+b-l[i+1])*inv100)%p
    A[n-1][n-1] = 1
    A[n][n] = p//(16)
    A = Matrix(A)
    B = A.LLL()
    h0 = B[0][-2]
    s0 = h0*(16)+l[0]
    seed2 = s0
    cracked = [l[0]]+[get_roll() for _ in range(29)]
    assert(cracked == out) # theres a chance to fail
    cracked = [get_roll() for _ in range(100)]

    proc.recvuntil(b"Now for the real challenge...")
    for j in cracked:
        real(j)
    proc.recvuntil(b"Alright, it seems that you can be trusted. Here's the secret: \n")
    print(proc.recvline().strip().decode())
