import random
from Crypto.Hash import keccak
from ecdsa import SECP256k1

curve = SECP256k1
G = curve.generator
q = curve.order

def solidity_keccak256(types, values):
    """abi.encodePacked + keccak256 for string, uint256 only."""
    encoded = b''
    for t, v in zip(types, values):
        if t == 'string':
            encoded += v.encode('utf-8')
        elif t == 'uint256':
            encoded += int(v).to_bytes(32, 'big')
    return keccak.new(digest_bits=256).update(encoded).digest()

def eth_message_hash(data: bytes) -> int:
    prefix = b"\x19Ethereum Signed Message:\n32"
    h = keccak.new(digest_bits=256)
    h.update(prefix + data)
    return int.from_bytes(h.digest(), 'big')

def generate_signature(private_key: int, types, values):
    max_nonce = 2**(256 - private_key % 102)
    k = random.randint(1, max_nonce - 1)

    raw_hash = solidity_keccak256(types, values)
    msg_hash_int = eth_message_hash(raw_hash)

    R = k * G
    r = R.x() % q
    s = (pow(k, -1, q) * (msg_hash_int + r * private_key)) % q
    v = 27 + (R.y() % 2)

    return (v, r, s)

