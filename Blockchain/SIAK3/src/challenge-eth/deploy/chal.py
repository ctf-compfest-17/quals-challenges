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
    (27, 0xcc01ccb300f10f031158676c41f6873354f95207c6e19fdce3a7f42af4d76691, 0xbbbe23505f16bf6eaa878d1b36cfb6cccc74abbdedb20d6b417373193186c32b, "2022-1"),
    (27, 0x97899d469d055b62c50d13443aee019f8028c1d577b665063062e841b57e8932, 0x33c543dea9078fbe23165ebfa039303db10b283be350b203db245db6f86ea341, "2022-2"),
    (27, 0xf720ecb1dad6068cf8196023e744f3cc503f836c1f29e56b1752ee074c3c59ed, 0xe38b09f7b09448bf8d0fed0fdb89a2a9eb92e593586999278deab6ee064eb50f, "2023-1"),
    (28, 0xdfa3554e4ec008d16ab70d538bb4955fba2edf50c807a84b60899d274e505128, 0x024d70376ac734255c41d6348eec0a093f2c6834067d0e4c47b4f34a5967b638, "2023-2"),
    (28, 0x23aa99b4d580123537705c790c9e3f691e97c17c7113d0320cbd221734edacbe, 0x3a12284ba4180b67d438942f92c62da87dc0adec9f9d3c4f85f3a3bc9f7e8356, "2024-1"),
    (27, 0xe7f9f89fa9ea62e94d93e05ab85245a710fb703a1df224edd7afaf35977c60d0, 0xf66749731a8592dd63e2371e4dc26edc4dd208e9c5daaf554906edc1fea7f181, "2024-2")
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