# FILE: chal.py (FINAL, CORRECTED VERSION)
import json
from pathlib import Path
import sandbox
from web3 import Web3

# --- Configuration & Pre-generated Signatures ---

# Private key for Bob's address (0x6dc7C25252515164FF388e10bB6dD1f5501fc88e)
BOB_PRIVKEY = "0xa4e8e4e8cafea0b69e4d1de7f98f5e159f07728f056a6405e68f2aa0b5607219"
BOB_ADDRESS = "0x6dc7C25252515164FF388e10bB6dD1f5501fc88e"

SIGNATURES_FOR_DEPLOYMENT = [
    (27, 0x4820336996035f1e326e4f3fe3bb2b897f1b0b18c1fe1128666cc11addc0cbc7, 0xf8394082e3e3619ebeae15d0616a9b7468c4e6e14ddd7e8b1820a7f1e9a01dbb, "2022-1"),
    (27, 0x6e0f5bf2a2216361047d782d1817b5aa420c1d1ff0471495bfb0972f4982a210, 0x7382d27b086d4f6c24abc6c78a6c482c1bdbe928bd9a50a0b3e62c0905fccf39, "2022-2"),
    (28, 0xa200cba9f24802fd3a993d7b0f2ab3676a42db7a47fe4cee796a56daad3923fc, 0x5ef132b9de2b39776470c5f393d83f5f56e443be6734d91611b09b7bf18d0de3, "2023-1"),
    (28, 0x2a2faa5395532d1e27dfde36d0be723073c7520aef8ccb6a2931c973b4992e3d, 0x31abb5757cd7f82042e7f1751ac13df375f7aafc5375fb881f1a2ef36f84ba52, "2023-2"),
    (28, 0x6716a65775f32fc47d310900d821d9f9a5080a90a753d91cc6e5f76795a889bd, 0x8d0c3119fd2a2aa7e3c351d48fb117b05aa1285a4f5f232d9c48fbc0ad92dbc2, "2024-1"),
    (27, 0xed882decbf926119b83ca108881ee17ec968ac23c8ddcdf193659434ede4083d, 0xd0230dce054212d837e37e1c3e14ea2cfe1b412453818e822c948b7123c0877d, "2024-2")
]

# --- Helper Function ---

def set_balance(web3: Web3, account_address: str, amount_wei: int):
    web3.provider.make_request("anvil_setBalance", [account_address, hex(amount_wei)])

# --- Main Deployment Logic ---

def deploy(web3: Web3, deployer_address: str, deployer_privateKey: str, player_address: str) -> str:
    # 1. Load Contract ABIs and Bytecode
    setup_info = json.loads(Path("compiled/Setup.sol/Setup.json").read_text())
    siak3_info = json.loads(Path("compiled/SIAK3.sol/SIAK3.json").read_text())
    
    # 2. Deploy the Setup Contract (which deploys SIAK3)
    setup_factory = web3.eth.contract(abi=setup_info["abi"], bytecode=setup_info["bytecode"]["object"])
    
    construct_txn = setup_factory.constructor().build_transaction({
        "from": deployer_address,
        "nonce": web3.eth.get_transaction_count(deployer_address),
        "value": Web3.to_wei(1, 'ether')
    })
    tx_hash = web3.eth.send_raw_transaction(web3.eth.account.sign_transaction(construct_txn, deployer_privateKey).raw_transaction)
    rcpt = web3.eth.wait_for_transaction_receipt(tx_hash)
    setup_address = rcpt.contractAddress
    
    setup_contract = web3.eth.contract(address=setup_address, abi=setup_info["abi"])
    siak3_address = setup_contract.functions.challenge().call()
    siak3_contract = web3.eth.contract(address=siak3_address, abi=siak3_info["abi"])

    # 3. Fund Bob and the Player so they can make transactions
    set_balance(web3, BOB_ADDRESS, Web3.to_wei(2, 'ether'))
    set_balance(web3, player_address, Web3.to_wei(2, 'ether'))

    # 4. Simulate Bob making all his past payments
    bob_nonce = web3.eth.get_transaction_count(BOB_ADDRESS)
    for v, r, s, semester in SIGNATURES_FOR_DEPLOYMENT:
        # THE FIX IS HERE: Convert Python int to bytes32 for r and s
        payment_txn = siak3_contract.functions.payTuition(
            v,
            r.to_bytes(32, 'big'),
            s.to_bytes(32, 'big'),
            semester
        ).build_transaction({
            "from": BOB_ADDRESS,
            "nonce": bob_nonce,
            "value": Web3.to_wei(0.1, 'ether'),
            "gas": 300000
        })
        signed_txn = web3.eth.account.sign_transaction(payment_txn, BOB_PRIVKEY)
        web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        web3.eth.wait_for_transaction_receipt(signed_txn.hash)
        bob_nonce += 1
    
    return setup_address

# --- Sandbox Launcher ---

app = sandbox.run_launcher(deploy)