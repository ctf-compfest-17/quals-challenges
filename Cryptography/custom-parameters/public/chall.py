
from Crypto.Util.number import getPrime,bytes_to_long
from random import randint
from math import gcd
FLAG = b"REDACTED"

def generate_pub_key():
    p = getPrime(2048)
    q = getPrime(2048)
    
    N = p * q

    phi = (p**2-1) * (q**2-1)
    while True:
        d = randint(phi-2**2048,phi-1)
        if gcd(d,phi) == 1:
            break
    e = pow(d,-1,phi)
    return N,e

def encrypt(m, N, e):
    m = bytes_to_long(m)
    ct = pow(m, e, N)
    return ct

if __name__ == "__main__":
    print("Generating public key....")
    print("")
    N, e= generate_pub_key()
    print("Done!")
    print("")
    m = FLAG
    ct = encrypt(m, N, e)
    with open("output.txt", "w") as f:
        f.write(f"N: {N}\n\n")
        f.write(f"e: {e}\n\n")
        f.write(f"ct: {ct}\n")

