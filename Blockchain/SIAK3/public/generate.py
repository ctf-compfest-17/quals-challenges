#!/usr/bin/env python3
import random
from Crypto.Hash import keccak
from ecdsa import SECP256k1, SigningKey

curve = SECP256k1
G = curve.generator
q = curve.order

NPM = "2206422922"
UKT_AMOUNT = 10**17
PAST_SEMESTERS = ["2022-1", "2022-2", "2023-1", "2023-2", "2024-1", "2024-2"]

bits = ?idkbro
nonce = 2**(256 - bits)
d = 0xbobprivatekey

sk = SigningKey.from_secret_exponent(d, curve=curve)
P = sk.get_verifying_key().pubkey.point
print(f"[*] Public Key (P): (0x{P.x():064x}, 0x{P.y():064x})")
print(f"[*] Private Key (d): (0x{d:064x})")

def solidity_keccak256(types, values):
    """Helper function to match Solidity's keccak256 packing."""
    encoded = b''
    for t, v in zip(types, values):
        if t == 'string': encoded += v.encode('utf-8')
        elif t == 'uint256': encoded += v.to_bytes(32, 'big')
    k_hash = keccak.new(digest_bits=256)
    k_hash.update(encoded)
    return int.from_bytes(k_hash.digest(), 'big')

random.seed(int(1337))

for i, semester in enumerate(PAST_SEMESTERS):
    k = random.randint(1, nonce - 1) 
    msg_hash_int = solidity_keccak256(['string', 'uint256', 'string'], [NPM, UKT_AMOUNT, semester])
    R = k * G
    r = R.x()
    s = (pow(k, -1, q) * (msg_hash_int + r * d)) % q
    v = 27 + (R.y() % 2)

    comma = "," if i < len(PAST_SEMESTERS) - 1 else ""
    print(f"({v}, 0x{r:064x}, 0x{s:064x}, \"{semester}\"){comma}")
