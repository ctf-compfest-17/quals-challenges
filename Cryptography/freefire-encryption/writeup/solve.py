from sage.all import *
from pwn import *
import os, ast
from lll_cvp import reduce_mod_p

io = remote("localhost", 1000)

p = 2**127 - 1
k = 64
F = GF((p, k), "x")

def to_list(el):
    return el.polynomial().padded_list(k)

def to_element(lst):
    return F(list(lst))

def get_pair():
    pt = os.urandom(32).hex().encode()
    io.sendlineafter('> ', pt)
    io.recvuntil('Encrypted: ')
    enc = ast.literal_eval(io.recvline().strip().decode())
    return to_element(pt), to_element(enc)

x1, y1 = get_pair()
x2, y2 = get_pair()
x3, y3 = get_pair()
z1 = x1 ** (p + 1)
z2 = x2 ** (p + 1)
z3 = x3 ** (p + 1)

A = matrix([
    [z1**2, z1, 1],
    [z2**2, z2, 1],
    [z3**2, z3, 1]
])
b = vector([y1, y2, y3])
c1, c2, c3 = A.solve_right(b)

x4, y4 = get_pair()
z4 = x4 ** (p + 1)
assert c1 * z4**2 + c2 * z4 + c3 == y4, "Prediction failed"

io.sendlineafter('> ', 'done')
io.recvuntil('Random: ')
rnd = bytes.fromhex(io.recvline().strip().decode())
z_rnd = to_element(rnd) ** (p + 1)
target = c1 * z_rnd**2 + c2 * z_rnd + c3
io.sendlineafter('Guess the random: ', ",".join(map(str, to_list(target))).encode())

io.recvuntil('Encrypted key: ')
enc_key = to_element(ast.literal_eval(io.recvline().strip().decode()))

discriminant = c2**2 - 4*c1*(c3 - enc_key)
sqrt_discriminant = discriminant.sqrt()

z1 = (-c2 + sqrt_discriminant) / (2*c1)
z2 = (-c2 - sqrt_discriminant) / (2*c1)

for z_cand in [z1, z2]:
    try:
        a = z_cand.nth_root(2**127)
        b = F(1).nth_root(2**127)
        sol_space = matrix([to_list(a * b**i) for i in range(1, 42)])
        
        if sol_space.rank() == 2:
            key = reduce_mod_p(sol_space[:2], p)[0]
            if key[0] < 0:
                key = -key
            
            key_bytes = bytes(key) if not isinstance(key, bytes) else key
            print(key_bytes.hex())
            io.sendlineafter('Guess the key: ', key_bytes.hex())
            io.interactive()
    except Exception as e:
        print(f"Error: {e}")
        continue