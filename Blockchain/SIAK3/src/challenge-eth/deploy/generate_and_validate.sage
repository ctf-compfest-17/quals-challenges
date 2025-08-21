#!/usr/bin/env sage
# FILE: generate_and_validate.sage (FULLY CORRECTED)

import random
from Crypto.Hash import keccak

# ======================================================================
# PART 0: CHALLENGE CONFIGURATION
# ======================================================================

# --- Cryptographic Parameters for secp256k1 ---
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
F = GF(p)
E = EllipticCurve(F, [0, 7])
G = E(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

# --- Challenge-Specific Private Key and Data ---
d = 0xa4e8e4e8cafea0b69e4d1de7f98f5e159f07728f056a6405e68f2aa0b5607219
P = d * G
NPM = "2206422922"
UKT_AMOUNT = 10**17
PAST_SEMESTERS = ["2022-1", "2022-2", "2023-1", "2023-2", "2024-1", "2024-2"]

# --- Nonce Bias Parameters ---
n_sigs = len(PAST_SEMESTERS)
bias_bits = d % 102
max_nonce = 2**(256 - bias_bits)
random.seed(int(1337))

print(f"[*] Using {n_sigs} signatures with a {bias_bits}-bit nonce bias.")

# ======================================================================
# PART 1: SIGNATURE GENERATION (Corrected)
# ======================================================================
print("\nPart 1: Generating biased signatures...")

def solidity_encode(types, values):
    """Encode same way as abi.encodePacked for string and uint256 only (as in your contract)."""
    encoded = b''
    for t, v in zip(types, values):
        if t == 'string':
            encoded += v.encode('utf-8')
        elif t == 'uint256':
            encoded += int(v).to_bytes(32, 'big')
        else:
            raise ValueError("unsupported type")
    return encoded

def keccak256_bytes(data: bytes) -> bytes:
    k = keccak.new(digest_bits=256)
    k.update(data)
    return k.digest()

signatures_for_attack = []
signatures_for_chal_py = []

for i in range(n_sigs):
    k = random.randint(1, max_nonce - 1)
    semester = PAST_SEMESTERS[i]

    raw_encoded = solidity_encode(['string', 'uint256', 'string'], [NPM, UKT_AMOUNT, semester])
    raw_hash = keccak256_bytes(raw_encoded)  # 32 bytes

    prefix = b"\x19Ethereum Signed Message:\n32"
    eth_signed = keccak256_bytes(prefix + raw_hash)
    msg_hash_int = Integer(int.from_bytes(eth_signed, 'big'))

    R = k * G
    r = Integer(R.xy()[0])
    # CORRECTED: All signature math must be modulo q
    s = (inverse_mod(k, q) * (msg_hash_int + r * d)) % q
    rec_id = Integer(R.xy()[1]) % 2
    v = 27 + rec_id
    signatures_for_attack.append((msg_hash_int, r, s))
    signatures_for_chal_py.append((v, r, s, semester))

print("Signatures generated. Copy the block below into your `chal.py`.")
print("-" * 60)
print("SIGNATURES_FOR_DEPLOYMENT = [")
for i, (v, r, s, sem) in enumerate(signatures_for_chal_py):
    comma = "," if i < len(signatures_for_chal_py) - 1 else ""
    print(f"    ({v}, 0x{r:064x}, 0x{s:064x}, \"{sem}\"){comma}")
print("]")
print("-" * 60)

# ======================================================================
# PART 2: LATTICE ATTACK VALIDATION (Corrected)
# ======================================================================
print("\nPart 2: Validating signatures with a lattice attack...")

n_attack = len(signatures_for_attack)
B = 2**(256 - bias_bits)

# CORRECTED: The lattice must also be constructed with modulo q
Mtilde_list = [B, 0]; Rtilde_list = [0, B/q]
for m, r, s in signatures_for_attack:
    s_inv = inverse_mod(s, q)
    Mtilde_list.append((s_inv * m) % q)
    Rtilde_list.append((s_inv * r) % q)

Mtilde = matrix(QQ, 1, len(Mtilde_list), Mtilde_list)
Rtilde = matrix(QQ, 1, len(Rtilde_list), Rtilde_list)
Pdiag = -q * identity_matrix(QQ, n_attack)
Z = matrix(QQ, n_attack, 2, 0)
M_lower = block_matrix([[Z, Pdiag]])
M = block_matrix([[Mtilde], [Rtilde], [M_lower]])

print("Running LLL")
L = M.LLL()

recovered_private_key = None
for row in L.rows():
    if recovered_private_key: break
    m, r, s = signatures_for_attack[0]
    candidate_k = row[2]
    for k_val in [candidate_k, -candidate_k]:
        if not k_val.is_integer() or k_val == 0: continue
        k = Integer(k_val)
        try:
            r_inv = inverse_mod(r, q)
            d_recovered = (r_inv * (k * s - m)) % q
            if d_recovered * G == P:
                recovered_private_key = d_recovered
                print("Nonce found! Key validated successfully.")
                break
        except (ZeroDivisionError, ValueError):
            continue

# ======================================================================
# PART 3: FINAL RESULT
# ======================================================================
if recovered_private_key:
    print("\n" + "=" * 60)
    print(f"Recovered Private Key: 0x{recovered_private_key:064x}")
    print("=" * 60)
else:
    print("\n" + "=" * 60)
    print("The lattice attack could not recover the private key.")
    print("=" * 60)