import json
from pathlib import Path
import hashlib
from eth_account import Account

import sandbox
from web3 import Web3

def set_balance(web3: Web3, account_address: str, amount: int):
    res = web3.provider.make_request(
        "anvil_setBalance",
        [account_address, amount]
    )
    print(res)


def postdeploy(web3: Web3, contract_address: str) -> str:
    private_key = hashlib.sha256(b"TalebPoastingSouthernEuropeanSquidInk").digest()
    account = Account.from_key(private_key)
    deployer_address = account.address
    
    set_balance(web3, deployer_address, Web3.to_wei(1, 'ether'))

    contract_info = json.loads(Path("compiled/Setup.sol/Setup.json").read_text())
    setup_abi = contract_info["abi"]
    setup_contract = web3.eth.contract(address=contract_address, abi=setup_abi)

    challenge_address = setup_contract.functions.challenge().call()
    print(f"Challenge contract address: {challenge_address}")

    vault_abi = [
        {
            "inputs": [
                {"name": "v", "type": "uint256"},
                {"name": "r", "type": "uint256"},
                {"name": "s", "type": "uint256"},
            ],
            "name": "claim_reward",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
    ]
    vault_contract = web3.eth.contract(address=challenge_address, abi=vault_abi)

    # Call claim_reward with predetermined v, r, s (to be replaced)
    v, r, s = 27, 84340066570771003327740667532724463987288408720245297984948571015505358516346, 20759614346651503343478388117300426381544956674102488141466218118965907459269
    print(f"Using v: {v}, r: {r}, s: {s}")

    #print deployer balance
    deployer_balance = web3.eth.get_balance(deployer_address)
    print(f"Deployer balance: {Web3.from_wei(deployer_balance, 'ether')} ether")

    tx_params = {
        "from": deployer_address,
        "nonce": web3.eth.get_transaction_count(deployer_address),
    }

    tx = vault_contract.functions.claim_reward(v, r, s).build_transaction(tx_params)
    
    signed_tx = account.sign_transaction(tx)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    print(f"Sent claim_reward transaction with hash: {tx_hash.hex()}")
    
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction receipt: {receipt}")


def deploy(web3: Web3, deployer_address: str, deployer_privateKey: str, player_address: str) -> str:
    uri = web3.provider.endpoint_uri
    contract_info = json.loads(Path("compiled/Setup.sol/Setup.json").read_text())
    abi = contract_info["abi"]
    bytecode = contract_info["bytecode"]["object"]

    contract = web3.eth.contract(abi=abi, bytecode=bytecode)

    set_balance(web3, deployer_address, Web3.to_wei(1000, 'ether'))

    construct_txn = contract.constructor().build_transaction(
        {
            "from": deployer_address,
            "nonce": web3.eth.get_transaction_count(deployer_address),
            "value": Web3.to_wei(80, 'ether'),  # Initial funding for the contract
        }
    )

    tx_create = web3.eth.account.sign_transaction(construct_txn, deployer_privateKey)
    tx_hash = web3.eth.send_raw_transaction(tx_create.raw_transaction)

    rcpt = web3.eth.wait_for_transaction_receipt(tx_hash)

    set_balance(web3, player_address, Web3.to_wei(100, 'ether'))

    print(f"Setup deployed at: {rcpt.contractAddress}")

    postdeploy(web3, rcpt.contractAddress)

    return rcpt.contractAddress

app = sandbox.run_launcher(deploy)