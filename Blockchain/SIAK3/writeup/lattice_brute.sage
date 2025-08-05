#!/usr/bin/env sage
# FILE: lattice_bruteforce.sage
# MODIFIED: This script iterates through possible nonce biases
# to find a private key containing the keyword "cafe".

from Crypto.Hash import keccak
import sys

# ======================================================================
# PART 1: PLAYER INPUT (Same as before)
# ======================================================================
SIGNATURES_RS = [
    (92275000740235486080370749874628753185212813837696037800776161417015351273105, 84918447355310604293623403096151950478500261589442703590194579974586716570411),
    (68542383661856809640594078590715824516846672499316634542898283958470010898738, 23416492569422210505794709877557202160415550533393694512789774176517838775105),
    (111779446313234233489542843877699106689583779874875228119625049163031568472557, 102920677163825577388050181850046615185211990065721669671549484743512982205711),
    (101154350065235955627579341714544689848687948015789746383570119719484298121512, 1041447410787426170440940437667102203983255225778983794716216031800524781112),
    (16132374543892311502637652879765370129675030514168542095186675784990694681790, 26266226574126440291485698136650155199503413066000517723420247130415088698198),
    (104925928879484075802059828334751100983589688009730257321371828387545500901584, 111451452929825956171821384519809767331310894729502922979075590171991076237697)
]
NPM = "2206422922"
UKT_AMOUNT = 10**17
PAST_SEMESTERS = ["2022-1", "2022-2", "2023-1", "2023-2", "2024-1", "2024-2"]

# --- Brute-force Parameters ---
# We will iterate through this range to find the correct bias
MIN_BIAS_BITS = 1
MAX_BIAS_BITS = 101
KEYWORD = "cafe"

# ======================================================================
# PART 2: BRUTE-FORCE ATTACK LOGIC
# ======================================================================

# --- secp256k1 Elliptic Curve Parameters ---
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
F = GF(p)
E = EllipticCurve(F, [0, 7])
G = E(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

def solidity_keccak256(types, values):
    encoded = b''
    for t, v in zip(types, values):
        if t == 'string': encoded += v.encode('utf-8')
        elif t == 'uint256': encoded += v.to_bytes(32, 'big')
    k_hash = keccak.new(digest_bits=256)
    k_hash.update(encoded)
    return int.from_bytes(k_hash.digest(), 'big')

print(f"⚙️  Starting private key recovery by brute-forcing bias_bits from {MIN_BIAS_BITS} to {MAX_BIAS_BITS}...")
print(f"[*] Searching for a private key containing the keyword: '{KEYWORD}'")

if not SIGNATURES_RS or len(SIGNATURES_RS) < 2:
    print("❌ Error: Please paste the (r, s) signature tuples from extract.py")
    sys.exit(1)

# 1. Recalculate message hashes (once is enough)
msg_hashes = [solidity_keccak256(['string', 'uint256', 'string'], [NPM, UKT_AMOUNT, s]) for s in PAST_SEMESTERS]
signatures_for_attack = []
for i in range(len(SIGNATURES_RS)):
    r_val, s_val = SIGNATURES_RS[i]
    h_val = msg_hashes[i]
    signatures_for_attack.append((h_val, r_val, s_val))

# --- The Main Brute-force Loop ---
for bias_bits in range(MIN_BIAS_BITS, MAX_BIAS_BITS + 1):
    print(f"\n[*] Trying bias_bits = {bias_bits}...")

    # 2. Construct the M-L lattice for the current bias
    n_attack = len(signatures_for_attack)
    B = 2**(256 - bias_bits)

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

    # 3. Run LLL reduction
    L = M.LLL()

    # 4. Find the private key from the short vector
    for row in L.rows():
        m, r, s = signatures_for_attack[0]
        candidate_k = row[2]
        
        for k_val in [candidate_k, -candidate_k]:
            if not k_val.is_integer() or k_val == 0: continue
            k = Integer(k_val)
            
            # A good check is to see if the recovered nonce k is within the current bias
            if k >= B: continue

            try:
                r_inv = inverse_mod(r, q)
                d_recovered = (r_inv * (k * s - m)) % q
                hex_d = f"0x{d_recovered:064x}"

                # --- CHECK FOR THE KEYWORD ---
                if KEYWORD in hex_d:
                    print("\n" + "=" * 60)
                    print("🎉🎉🎉      KEYWORD FOUND!      🎉🎉🎉")
                    print(f"Success with bias_bits: {bias_bits}")
                    print(f"Recovered Private Key (hex): {hex_d}")
                    print(f"Recovered Private Key (int): {d_recovered}")
                    print("=" * 60)
                    #sys.exit(0) # Exit successfully
                    continue

            except (ZeroDivisionError, ValueError):
                continue

# If the loop finishes without finding the key
print("\n" + "=" * 60)
print("❌❌❌      ATTACK FAILED      ❌❌❌")
print("Could not find a key containing the keyword in the specified bias range.")
print("=" * 60)
