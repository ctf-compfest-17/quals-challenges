
from Crypto.Util.number import getPrime,bytes_to_long
from random import randint
from math import gcd
from decimal import Decimal
FLAG = b"COMPFEST17{wienner_attack_also_works_on_too_large_d_with_a_bit_of_a_twist_6fe4dd8e23}"

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
    with open("../public/output.txt", "w") as f:
        f.write(f"N: {N}\n\n")
        f.write(f"e: {e}\n\n")
        f.write(f"ct: {ct}\n")

