import random

coeffs = []
for i in range(5):
    coeffs.append(random.getrandbits(1024))

g = random.getrandbits(512)
x = random.getrandbits(512)
y = random.getrandbits(512)