import random
from decimal import Decimal, getcontext
from math import isqrt
from Crypto.Util.number import getPrime, GCD, bytes_to_long
def normal(N):
    nd = len(str(N))
    getcontext().prec = max(80, nd*2)
    Ndec = Decimal(N)
    val = Decimal(2)*Ndec - Decimal(4)*(Decimal(2).sqrt())*(Ndec ** (Decimal(3)/Decimal(4)))
    if val <= 0:
        return 1
    return int(val)  # floor

def generate_key(nbits=4096, v_attempts=64):
    half = nbits//2
    p = getPrime(half)
    q = getPrime(half)
    while q == p:
        q = getPrime(half)
    N = p * q
    phi = (p**2 - 1) * (q**2 - 1)

    thr = normal(N)

    d_max = max(2, isqrt(thr))
    for _ in range(10000):
        d = random.randrange(2, d_max + 1)
        if GCD(d, phi) == 1:
            break

    found = False
    for _ in range(v_attempts):
        v_max = thr // d - 1
        if v_max < 2:
            for _ in range(1000):
                d = random.randrange(2, d_max + 1)
                if GCD(d, phi) == 1:
                    break
            v_max = thr // d - 1
            if v_max < 2:
                continue
        v = random.randrange(2, v_max + 1)
        e0 = (phi * v) // d
        if e0 < 2:
            continue
        w0 = e0 * d - phi * v
        if v * N <= abs(w0):
            continue
        for t in range(-1024, 1025):
            e = e0 + t
            if e < 2:
                continue
            if GCD(e, phi) != 1:
                continue
            w = e * d - phi * v
            if abs(w) < v * N and d * v < thr:
                found = True
                break
        if found:
            break

    return N, e

if __name__ == "__main__":
    N, e = generate_key()
    FLAG = b"REDACTED"
    m = bytes_to_long(FLAG)
    ct = pow(m, e, N)
    with open("output.txt", "w") as f:
        f.write(f"N: {N}\n\n")
        f.write(f"e: {e}\n\n")
        f.write(f"ct: {ct}\n")

