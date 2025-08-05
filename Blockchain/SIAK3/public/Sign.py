import random
from Crypto.Hash import keccak
from ecdsa import SECP256k1

curve = SECP256k1
G = curve.generator
q = curve.order

def solidity_keccak256(types, values):
    """Helper function to match Solidity's keccak256 packing."""
    encoded = b''
    for t, v in zip(types, values):
        if t == 'string': encoded += v.encode('utf-8')
        elif t == 'uint256': encoded += v.to_bytes(32, 'big')
    k_hash = keccak.new(digest_bits=256)
    k_hash.update(encoded)
    return int.from_bytes(k_hash.digest(), 'big')

def generate_signature(private_key, types, values):
    d = private_key
    nonce = 2**(256 - private_key % 102)
    k = random.randint(1, nonce - 1) 
    msg_hash_int = solidity_keccak256(types, values)
    R = k * G
    r = R.x()
    s = (pow(k, -1, q) * (msg_hash_int + r * d)) % q
    v = 27 + (R.y() % 2)

    return (v, r, s)
