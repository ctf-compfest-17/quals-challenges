#!/usr/bin/env sage

from Crypto.Hash import keccak
import sys
from sage.all import Integer, GF, EllipticCurve, matrix, block_matrix, identity_matrix, QQ, inverse_mod

# ======================================================================
# PART 1: PLAYER INPUT
# ======================================================================
SIGNATURES_RS = [
    (92275000740235486080370749874628753185212813837696037800776161417015351273105, 938387978576515701635573527877198814027156505126201817458405595763218205748),
    (68542383661856809640594078590715824516846672499316634542898283958470010898738, 55701524931721558714461330947112418182546493739714441466748159369496411213437),
    (111779446313234233489542843877699106689583779874875228119625049163031568472557, 56114346837905865424250582499044528454999491893556622126051851657460983316852),
    (101154350065235955627579341714544689848687948015789746383570119719484298121512, 1140893849393957732871666834426205475508037270320744184361072275259442400794),
    (16132374543892311502637652879765370129675030514168542095186675784990694681790, 49550853042178331912203460103493019263587616818361274861263284823208849102013),
    (104925928879484075802059828334751100983589688009730257321371828387545500901584, 75840292335711683573308945467091408659005053035973039543662880747803372331658)
]
NPM = "2206422922"
UKT_AMOUNT = 10**17
PAST_SEMESTERS = ["2022-1", "2022-2", "2023-1", "2023-2", "2024-1", "2024-2"]

# --- Brute-force Parameters ---
MIN_BIAS_BITS = 1
MAX_BIAS_BITS = 101
KEYWORD = "cafe"

# ======================================================================
# PART 2: EC PARAMETERS
# ======================================================================
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
F = GF(p)
E = EllipticCurve(F, [0, 7])
G = E(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
          0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

def solidity_encode(types, values):
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
    h = keccak.new(digest_bits=256)
    h.update(data)
    return h.digest()

print(f"Starting private key recovery by brute-forcing bias_bits from {MIN_BIAS_BITS} to {MAX_BIAS_BITS}...")
print(f"Searching for a private key containing the keyword: '{KEYWORD}'")

if not SIGNATURES_RS or len(SIGNATURES_RS) < 2:
    print("Error: Please paste the (r, s) signature tuples from extract.py")
    sys.exit(1)

msg_hashes = []
for semester in PAST_SEMESTERS:
    raw = solidity_encode(['string', 'uint256', 'string'], [NPM, UKT_AMOUNT, semester])
    raw_hash = keccak256_bytes(raw)
    prefix = b"\x19Ethereum Signed Message:\n32"
    eth_prefixed = keccak256_bytes(prefix + raw_hash)  
    m_int = Integer(int.from_bytes(eth_prefixed, 'big'))
    msg_hashes.append(m_int)

signatures_for_attack = []
for i in range(len(SIGNATURES_RS)):
    r_val, s_val = SIGNATURES_RS[i]
    m_val = msg_hashes[i]
    signatures_for_attack.append((m_val, Integer(r_val), Integer(s_val)))

for bias_bits in range(MIN_BIAS_BITS, MAX_BIAS_BITS + 1):
    print(f"\n[*] Trying bias_bits = {bias_bits}...")

    n_attack = len(signatures_for_attack)
    B = Integer(2)**(256 - bias_bits)

    Mtilde_list = [Integer(B), Integer(0)]
    Rtilde_list = [Integer(0), Integer(B) / Integer(q)]
    for m, r, s in signatures_for_attack:
        s_inv = inverse_mod(s, Integer(q))
        Mtilde_list.append((s_inv * m) % Integer(q))
        Rtilde_list.append((s_inv * r) % Integer(q))

    Mtilde = matrix(QQ, 1, len(Mtilde_list), [Integer(x) for x in Mtilde_list])
    Rtilde = matrix(QQ, 1, len(Rtilde_list), [QQ(x) for x in Rtilde_list])
    Pdiag = -Integer(q) * identity_matrix(QQ, n_attack)
    Z = matrix(QQ, n_attack, 2, 0)
    M_lower = block_matrix([[Z, Pdiag]])
    M = block_matrix([[Mtilde], [Rtilde], [M_lower]])

    L = M.LLL()

    found_any = False
    for row in L.rows():
        try:
            candidate_k = Integer(row[2])
        except Exception:
            continue

        for k_val in [candidate_k, -candidate_k]:
            if not k_val.is_integer() or k_val == 0:
                continue
            k = Integer(k_val)

            if abs(k) >= B:
                continue

            m0, r0, s0 = signatures_for_attack[0]
            try:
                r0_inv = inverse_mod(r0, Integer(q))
                d_recovered = (r0_inv * (k * s0 - m0)) % Integer(q)
                hex_d = f"0x{int(d_recovered):064x}"

                if KEYWORD in hex_d:
                    print("\n" + "=" * 60)
                    print("KEYWORD FOUND!")
                    print(f"Success with bias_bits: {bias_bits}")
                    print(f"Recovered Private Key (hex): {hex_d}")
                    print(f"Recovered Private Key (int): {int(d_recovered)}")
                    print("=" * 60)
                    
            except Exception:
                continue



