
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes
from random import randint
from math import gcd
from decimal import Decimal
FLAG = b"COMPFEST17{63n3r4l1z3d_w13n3r_4774ck_4641n57_700_l4r63_d_15_c00l_e97e4f3392}"

def generate_pub_key():
    while True:
        p = getPrime(2048)
        q = getPrime(2048)
        if (p < q < 2*p) or (q< p < 2*q):
            break
    N = p * q
    phi = (p**2-1) * (q**2-1)
    bound = round((Decimal(2*N).sqrt()).sqrt())
    while True:
        d = randint(phi-bound,phi-1)
        if gcd(d,phi) == 1:
            break
    e = pow(d,-1,phi)
    return N,e,d

def encrypt(m, N, e):
    m = bytes_to_long(m)
    ct = pow(m, e, N)
    return ct

if __name__ == "__main__":
    print("Generating public key....")
    print("")
    N, e,d= generate_pub_key()
    print("Done!")
    print("")
    m = FLAG
    ct = encrypt(m, N, e)
    print("N:", N)
    print("e:", e)
    print("ct:", ct)

