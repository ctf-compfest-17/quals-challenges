# FILE: extract.py (FINAL, CORRECTED VERSION)
import json
from web3 import Web3

# ======================================================================
# CONFIGURATION
# ======================================================================
# --- UPDATE THESE VALUES FOR YOUR DEPLOYMENT ---
RPC_URL = "http://127.0.0.1:48334/452bc267-3e75-49ad-9172-5155ea0a6e94"
PRIVKEY = "0f8f8e8e0903c378cfdf7e5fd2932d509babfa14dc676fbfad535b868328e667"
SETUP_CONTRACT_ADDR = "0x4c49B0442E89cac3b9dED944f8f2f5dBb1f3970b"
WALLET_ADDR = "0xF0B10f6d9A8Ab64Dfe33F57B3DFcE6E4782BE2eE"
# -----------------------------------------------

# --- ABIs for the Tuition Payment Challenge (Updated for final contracts) ---
SETUP_ABI = json.loads('''
[
    {"inputs":[],"name":"challenge","outputs":[{"internalType":"contract SIAK3","name":"","type":"address"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"isSolved","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}
]
''')

SIAK3_ABI = json.loads('''
[
    {"inputs":[],"name":"CURRENT_SEMESTER","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"NPM","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"STUDENT_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"UKT_AMOUNT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"isChallengeSolved","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"paidSemesters","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},
    {"inputs":[],"name":"pastPaymentCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},
    {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"pastPayments","outputs":[{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"},{"internalType":"string","name":"semester","type":"string"}],"stateMutability":"view","type":"function"}
]
''')
# ======================================================================

def main():
    # Connect to the blockchain
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        print(f"❌ Failed to connect to RPC URL: {RPC_URL}")
        return

    print(f"✓ Connected to: {w3.provider.endpoint_uri}")
    print(f"✓ Setup Contract: {SETUP_CONTRACT_ADDR}")
    print("-" * 60)

    # Get contract instances
    setup_contract = w3.eth.contract(address=Web3.to_checksum_address(SETUP_CONTRACT_ADDR), abi=SETUP_ABI)
    siak3_address = setup_contract.functions.challenge().call()
    siak3_contract = w3.eth.contract(address=siak3_address, abi=SIAK3_ABI)
    print(f"✓ SIAK3 Contract: {siak3_address}")

    # Get public data from the contract
    student_address = siak3_contract.functions.STUDENT_ADDRESS().call()
    npm = siak3_contract.functions.NPM().call()
    ukt_amount = siak3_contract.functions.UKT_AMOUNT().call()
    current_semester = siak3_contract.functions.CURRENT_SEMESTER().call()

    print(f"✓ Student Address: {student_address}")
    print(f"✓ NPM: {npm}")
    print(f"✓ UKT Amount: {ukt_amount} wei")
    print(f"✓ Target Semester: {current_semester}")
    print("-" * 60)

    # Extract all past payment signatures
    payment_count = siak3_contract.functions.pastPaymentCount().call()
    if payment_count == 0:
        print("❌ No payment records found in the contract.")
        return

    print(f"Found {payment_count} historical payment records to extract...")

    signatures_for_attack = []
    for i in range(payment_count):
        try:
            # CORRECTED: Call the public getter for the `pastPayments` mapping
            v, r_bytes, s_bytes, semester = siak3_contract.functions.pastPayments(i).call()

            # Convert bytes32 to integers for the attack script
            r_int = int.from_bytes(r_bytes, 'big')
            s_int = int.from_bytes(s_bytes, 'big')

            signatures_for_attack.append((r_int, s_int))
            print(f"  > Extracted signature for semester '{semester}'")

        except Exception as e:
            print(f"❌ Error retrieving payment record {i}: {e}")
            break

    print("-" * 60)
    print("✓ EXTRACTION COMPLETE")
    print("-" * 60)
    print("Copy the following list into your `attack.sage` script:\n")

    # Print the final formatted list for direct use in attack.sage
    print("SIGNATURES_RS = [")
    for i, (r, s) in enumerate(signatures_for_attack):
        comma = "," if i < len(signatures_for_attack) - 1 else ""
        print(f"    ({r}, {s}){comma}")
    print("]")

if __name__ == "__main__":
    main()

