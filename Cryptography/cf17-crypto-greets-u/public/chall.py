from Crypto.Util.number import bytes_to_long, getPrime
from secret import coeffs, g, x, y
import random
import os

with open('flag.txt', 'rb') as f:
    flag = f.read().strip()

random.seed(os.urandom(128))
m = bytes_to_long(flag)
p = getPrime(30)
e = 5
k = 100
n = p**k

poly_result = 0
for i in range(e):
    poly_result = (poly_result + coeffs[i] * pow(m, i, n)) % n

h = pow(g, x, n) 

test_msg = bytes_to_long(b"This is just a test message.")
c1_test = pow(g, y, n)
s_test = pow(h, y, n)
c2_test = (test_msg * s_test) % n

c1_secret = pow(g, y, n) 
s_secret = pow(h, y, n)  
c2_secret = (poly_result * s_secret) % n

for i in range(19968):
    if random.getrandbits(32) % 2 == 0:
        print("even")
    else:
        print("odd")
        
print(f"p = {p}")
print(f"e = {e}")
print(f"n = {n}")
print(f"coeffs = {coeffs}")
print(f"c1_test = {c1_test + random.getrandbits(1024)}")
print(f"c2_test = {c2_test + random.getrandbits(1024)}")
print(f"c1_secret = {c1_secret + random.getrandbits(1024)}")
print(f"c2_secret = {c2_secret + random.getrandbits(1024)}")