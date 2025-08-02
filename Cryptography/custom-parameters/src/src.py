
from Crypto.Util.number import getPrime,bytes_to_long
from random import randint
from math import gcd
FLAG = b"COMPFEST17{wait__that_works_here_too__thats_cool_anyway_see_you_at_the_finals_75d3e3d44a}"

def generate_pub_key():
    while True:
        p = getPrime(2048)
        q = getPrime(2048)
        if (p < q < 2*p) or (q< p < 2*q):
            break
    N = p * q
    phi = (p**2-1) * (q**2-1)
    print("N: ", N)
    bound = int(input("Enter bound: "))
    while True:
        d = randint(phi-bound,phi-1)
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
    print("e:", e)
    print("ct:", ct)

