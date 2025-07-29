#!/usr/bin/env sage
# FILE: lattice.sage (CORRECTED PLAYER EXPLOIT)

from Crypto.Hash import keccak

# ======================================================================
# PART 1: PLAYER INPUT
# ======================================================================
# --- Step 1: Run `python3 extract.py` and paste the output here ---
SIGNATURES_RS = [
    (32623419039724405358361730231518723064068357738380964182016196578913638468551, 112274741971901123010874496447088390224402622393849458590586967369597205880251),
    (49781550650429956236528405422352507828103602525477950430543099767599053054480, 52247120389190556663169277729823222353936975082181780198048902851991791521593),
    (73276087106743738618627770318635577104990863385247669369909693872211358196732, 42943568007743214350897101588710223593554393645319133598390522683148567645667),
    (19081357002822048324199195650183931756679567054181696077379560280174594960957, 22466712812207254659321878161546911567812538461337016734136490268994199403090),
    (46628242087332069019945759487018122821634103945312359257821715453622734064061, 63797652701248916924240706621906924160100687621637248102209031566058924989378),
    (107438753276351877995694537697477531064141275386292628822758556994725212325949, 94143007429591916509195617963770697106672613093266106983461899701132963383165)
]

# --- Step 2: Fill in known public data ---
NPM = "2206422922"
UKT_AMOUNT = 10**17
PAST_SEMESTERS = ["2022-1", "2022-2", "2023-1", "2023-2", "2024-1", "2024-2"]
CURRENT_SEMESTER = "2025-1"

# --- Step 3: Set the nonce bias ---
bias_bits = 50

# ======================================================================
# PART 2: ATTACK LOGIC (M-L Formulation)
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

print("⚙️  Starting private key recovery...")

if not SIGNATURES_RS or len(SIGNATURES_RS) < 2:
    print("❌ Error: Please paste the (r, s) signature tuples from extract.py")
    exit()

# 1. Recalculate message hashes
msg_hashes = [solidity_keccak256(['string', 'uint256', 'string'], [NPM, UKT_AMOUNT, s]) for s in PAST_SEMESTERS]
print(f"✓ Calculated {len(msg_hashes)} message hashes.")

# Combine r, s, and hashes for the attack
signatures_for_attack = []
for i in range(len(SIGNATURES_RS)):
    r_val, s_val = SIGNATURES_RS[i]
    h_val = msg_hashes[i]
    signatures_for_attack.append((h_val, r_val, s_val))

# 2. Construct the M-L lattice
n_attack = len(signatures_for_attack)
B = 2**(256 - bias_bits)
print(f"Building {n_attack+2}x{n_attack+2} matrix...")

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
print("✓ Matrix constructed.")

# 3. Run LLL reduction
print("✓ Running LLL reduction...")
L = M.LLL()
print("✓ LLL reduction complete.")

# 4. Find the private key from the short vector
print("✓ Searching for the private key in the reduced basis...")
recovered_private_key = -1
for row in L.rows():
    if recovered_private_key != -1: break
    m, r, s = signatures_for_attack[0]
    candidate_k = row[2]
    for k_val in [candidate_k, -candidate_k]:
        if not k_val.is_integer() or k_val == 0: continue
        k = Integer(k_val)
        try:
            r_inv = inverse_mod(r, q)
            d_recovered = (r_inv * (k * s - m)) % q
            # We don't have the public key, so we can't validate.
            # But the short vector from LLL is almost certainly the right one.
            # A good check is to see if the recovered nonce k is within the bias.
            if k < B:
                recovered_private_key = d_recovered
                print("✓ Potential nonce found! Assuming key is correct.")
                break
        except (ZeroDivisionError, ValueError):
            continue

if recovered_private_key == -1:
    print("\n❌ Attack failed: Could not find the private key.")
    exit()

print("\n" + "=" * 60)
print("🔑      PRIVATE KEY RECOVERED      🔑")
print(f"Recovered Private Key (int): {recovered_private_key}")
print(f"Recovered Private Key (hex): 0x{recovered_private_key:064x}")
print("=" * 60)


# ======================================================================
# PART 3: FORGE SIGNATURE FOR THE CURRENT SEMESTER
# ======================================================================
print("\n⚙️  Forging signature for the current semester to solve the challenge...")
k_forge = int.from_bytes(solidity_keccak256(['uint256', 'string'], [recovered_private_key, CURRENT_SEMESTER]).to_bytes(32, 'big'), 'big') % q
current_hash = solidity_keccak256(['string', 'uint256', 'string'], [NPM, UKT_AMOUNT, CURRENT_SEMESTER])
R_final = k_forge * G
r_final = Integer(R_final.xy()[0])
s_final = (inverse_mod(k_forge, q) * (current_hash + r_final * recovered_private_key)) % q
rec_id_final = Integer(R_final.xy()[1]) % 2
v_final = 27 + rec_id_final

print("\n" + "=" * 60)
print("🎉      SOLUTION SIGNATURE      🎉")
print(f"Use these values to call payTuition('{CURRENT_SEMESTER}')")
print(f"v: {v_final}")
print(f"r: 0x{r_final:064x}")
print(f"s: 0x{s_final:064x}")
print("=" * 60)
