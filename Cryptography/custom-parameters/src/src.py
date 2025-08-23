
from Crypto.Util.number import getPrime,bytes_to_long
from random import randint
from math import gcd
from decimal import Decimal
FLAG = b"COMPFEST17{wait__that_works_here_too__thats_cool_anyway_see_you_at_the_finals_75d3e3d44a}"

def generate_pub_key():
    
    p = getPrime(2048)
    q = getPrime(2048)

    N = p * q
    
    print("N: ", N)

    phi = (p**2-1) * (q**2-1)
    
    bound = int(input("Enter bound: "))
    if bound < 2**1000:
        print("Get out of here!")
        exit(1)
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

