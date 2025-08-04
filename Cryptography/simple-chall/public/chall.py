from Crypto.Util.Padding import pad
from Crypto.Util.number import inverse, getPrime
from Crypto.Cipher import AES
import hashlib, random, math

flag = b"COMPFEST17{REDACTED}"

def generate_key(n):
    priv_key = []
    for i in range(n):
        priv_key.append(random.randint(0, 1))
    return priv_key

def generate_given(bound, mod, k, n, priv_key):
    a = []
    for i in range(k):
        row = []
        for i in range(n):
            row.append(random.randint(1, int(math.sqrt(mod // 4096))))
        a.append(row)

    b = []
    for i in a:
        total = 0
        for p, ai in zip(priv_key, i):
            total += p * ai

        assert total <= bound
        while True:
            g = random.randint(int(math.sqrt(mod // 4)), int(math.sqrt(mod // 2)))
            if math.gcd(total, g) == 1:
                break
        
        f = (inverse(total, mod) * g) % mod
        b.append(f)
    
    return a, b

def encrypt(msg, key):
    msg = pad(msg, 16)
    key = hashlib.sha256(bytes(key)).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    ct = cipher.encrypt(msg)
    return ct

if __name__ == "__main__":
    k, n = 64, 128
    mod = getPrime(1024)
    bound = int(math.sqrt(mod//2))

    private_key = generate_key(n)
    a, b = generate_given(bound, mod, k, n, private_key)

    ciphertext = encrypt(flag, private_key)
    with open('encrypted.txt', 'w') as f:
        f.write("Ciphertext: " + ciphertext.hex() + "\n")
        f.write("Modulo: " + str(mod) + "\n")
        f.write("Given1: [" + ", ".join([str(i) for i in a]) + "]\n")
        f.write("Given2: [" + ", ".join([str(i) for i in b]) + "]\n")