from Crypto.Util.number import bytes_to_long, getPrime
import random

with open('flag.txt', 'rb') as f:
    flag = f.read().strip()

m = bytes_to_long(flag)
p = getPrime(32)
e = 5
k = 100
n = p**k

coeffs = []
for i in range(e):
    coeffs.append(random.randint(1, n-1))

poly_result = 0
for i in range(e):
    poly_result = (poly_result + coeffs[i] * pow(m, i, n)) % n

g = random.randint(2, n-1)
x = random.randint(2, n-2)
y = random.randint(2, n-2)
h = pow(g, x, n) 

test_msg = bytes_to_long(b"This is just a test message.")
c1_test = pow(g, y, n)
s_test = pow(h, y, n)
c2_test = (test_msg * s_test) % n

c1_secret = pow(g, y, n) 
s_secret = pow(h, y, n)  
c2_secret = (poly_result * s_secret) % n

print(f"p = {p}")
print(f"e = {e}")
print(f"n = {n}")
print(f"coeffs = {coeffs}")
print(f"g = {g}")
print(f"h = {h}")
print(f"c1_test = {c1_test}")
print(f"c2_test = {c2_test}")
print(f"c1_secret = {c1_secret}")
print(f"c2_secret = {c2_secret}")