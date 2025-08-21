# FILE: extract.py
# Extract signatures from SIAK3 contract for cryptanalysis

import json
from web3 import Web3

# ======================================================================
# CONFIGURATION
# ======================================================================
RPC_URL = "http://127.0.0.1:48334/a0b8d49b-bf4a-4401-a449-380936057469"
PRIVKEY = "a5ea873693f14693d42ace45da0bff4c87bd630c4b1bb97090592ad92df4dce7"
SETUP_CONTRACT_ADDR = "0xa7B1760E62EDA5dF60214A187cbCf8AF741BD504"
WALLET_ADDR = "0xB03ffB7D9E781A76668f75920c7d4b8c76C3b574"
# ======================================================================

SETUP_ABI = json.loads('''
[
    {"inputs":[],"name":"challenge","outputs":[{"internalType":"contract SIAK3","name":"","type":"address"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"isSolved","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}
]
''')

SIAK3_ABI = json.loads('''
[
    {"inputs":[],"name":"STUDENT_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"NPM","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"UKT_AMOUNT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"paidSemesters","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"PaymentCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"Payments","outputs":[{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"},{"internalType":"string","name":"semester","type":"string"}],"stateMutability":"view","type":"function"}
]
''')

def main():
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        print(f"[!] Failed to connect to RPC at {RPC_URL}")
        return

    setup_contract = w3.eth.contract(address=Web3.to_checksum_address(SETUP_CONTRACT_ADDR), abi=SETUP_ABI)
    siak3_address = setup_contract.functions.challenge().call()
    siak3_contract = w3.eth.contract(address=siak3_address, abi=SIAK3_ABI)

    print(f"[+] Connected")
    print(f" Setup Contract : {SETUP_CONTRACT_ADDR}")
    print(f" SIAK3 Contract : {siak3_address}")
    print("-" * 60)

    # Read contract constants
    student_address = siak3_contract.functions.STUDENT_ADDRESS().call()
    npm = siak3_contract.functions.NPM().call()
    ukt_amount = siak3_contract.functions.UKT_AMOUNT().call()

    print(f" Student Address : {student_address}")
    print(f" NPM             : {npm}")
    print(f" UKT Amount      : {ukt_amount} wei")
    print("-" * 60)

    # Extract all payment records
    payment_count = siak3_contract.functions.PaymentCount().call()
    if payment_count == 0:
        print("[!] No payments found, nothing to extract")
        return

    print(f"[+] Found {payment_count} payment records\n")

    signatures = []
    for i in range(payment_count):
        try:
            v, r_bytes, s_bytes, semester = siak3_contract.functions.Payments(i).call()

            r = int.from_bytes(r_bytes, "big")
            s = int.from_bytes(s_bytes, "big")

            signatures.append((r, s, v, semester))
            print(f" #{i} Semester '{semester}' | v={v}, r={hex(r)}, s={hex(s)}")

        except Exception as e:
            print(f"[!] Error reading payment {i}: {e}")
            break

    print("\n" + "=" * 60)
    print("Copy the following list into your Sage attack script:")
    print("=" * 60)
    print("SIGNATURES_RS = [")
    for i, (r, s, v, semester) in enumerate(signatures):
        comma = "," if i < len(signatures) - 1 else ""
        print(f"    ({r}, {s}){comma}  # semester {semester}, v={v}")
    print("]")

if __name__ == "__main__":
    main()
