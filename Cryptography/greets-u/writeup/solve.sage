from sage.all import *
from Crypto.Util.number import long_to_bytes, bytes_to_long
from pwn import *
from tqdm import tqdm, trange

def elgamal_nonce_reuse_attack(n, test_msg, c1_test, c2_test, c1_secret, c2_secret):
    """
    Recovers secret message when same nonce is used in ElGamal
    """
    s = (c2_test * pow(test_msg, -1, n)) % n
    secret_msg = (c2_secret * pow(s, -1, n)) % n
    return int(secret_msg)

def lift(f, p, k, previous):
    result = []
    df = diff(f)
    for lower_solution in previous:
        dfr = Integer(df(lower_solution))
        fr = Integer(f(lower_solution))
        if dfr % p != 0:
            t = (-(xgcd(dfr, p)[1]) * int(fr / p ** (k - 1))) % p
            result.append(lower_solution + t * p ** (k - 1))
        if dfr % p == 0:
            if fr % p ** k == 0:
                for t in range(0, p):
                    result.append(lower_solution + t * p ** (k - 1))
    return result

def hensel_lifting(f, p, k, base_solution):
    solution = base_solution
    for i in tqdm(range(2, k + 1), desc="Hensel Lifting"):
        solution = lift(f, p, i, solution)
    return solution

def construct_a_row(RNG):
    row = []
    for _ in range(19968):
        out = RNG.getrandbits(32)
        row.append(out & 1)
    return row

print("[*] Building matrix L...")
L = Matrix(GF(2), 19968, 19968, sparse=True)
RNG = random.Random()

for i in trange(19968):
    state = [0] * 624
    temp = "0" * i + "1" + "0" * (19968 - 1 - i)
    for j in range(624):
        state[j] = int(temp[32*j:32*j+32], 2)
    RNG.setstate((3, tuple(state + [624]), None))
    row = construct_a_row(RNG)
    L[i] = row

print("[*] Transforming matrix...")
M = L.transpose()

M = M[:19968, [0] + list(range(32, 19968))]

print("[*] Matrix M shape:", M.nrows(), "x", M.ncols())

io = process(['python', 'chall.py'])

leak_bits = []
for _ in range(19968):
    if io.recvline().strip() == b"even":
        leak_bits.append(0)
    else:
        leak_bits.append(1)

io.recvuntil(b'p = ')
p = int(io.recvline().strip())

io.recvuntil(b'e = ')
e = int(io.recvline().strip())

io.recvuntil(b'n = ')
n = int(io.recvline().strip())

io.recvuntil(b'coeffs = ')
coeffs = eval(io.recvline().strip())

test_msg = bytes_to_long(b"This is just a test message.")

io.recvuntil(b'c1_test = ')
c1_test = int(io.recvline().strip())

io.recvuntil(b'c2_test = ')
c2_test = int(io.recvline().strip())

io.recvuntil(b'c1_secret = ')
c1_secret = int(io.recvline().strip())

io.recvuntil(b'c2_secret = ')
c2_secret = int(io.recvline().strip())

assert len(leak_bits) == 19968, f"Expected 19968 bits, got {len(leak_bits)}"

print("[*] Solving for MT state...")
R = vector(GF(2), leak_bits)
res = (M.solve_right(R)).list()  

# Rebuild MT internal state
res = [res[0]] + [0] * 31 + res[1:]
init_bits = "".join(map(str, res))
state_words = [int(init_bits[32*i:32*i+32], 2) for i in range(624)]

RNG = random.Random()
RNG.setstate((3, tuple(state_words + [624]), None))
for _ in range(19968):RNG.getrandbits(32)

c1_test -= RNG.getrandbits(1024)
c2_test -= RNG.getrandbits(1024)
c1_secret -= RNG.getrandbits(1024)
c2_secret -= RNG.getrandbits(1024)

poly_result = elgamal_nonce_reuse_attack(n, test_msg, c1_test, c2_test, c1_secret, c2_secret)
print(f"Recovered polynomial result: {poly_result}")

P_base = PolynomialRing(Zmod(p), 'x')
x = P_base.gen()
f_base = sum(coeffs[i] * x^i for i in range(e)) - poly_result

base_solutions = []
for i in tqdm(range(p), desc="Finding base solutions"):
    if f_base(i) == 0:
        base_solutions.append(i)

k = 100
N = p^k
P = PolynomialRing(Zmod(N), 'x', implementation='NTL')
x = P.gen()
f = sum(coeffs[i] * x^i for i in range(e)) - poly_result

solutions = hensel_lifting(f, p, k, base_solutions)

for solution in solutions:
    try:
        flag = long_to_bytes(int(solution))
        if b'COMPFEST' in flag:
            print(f"Flag found: {flag}")
            break
    except:
        pass