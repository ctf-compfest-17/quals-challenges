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


def predeploy(web3: Web3) -> str:
    private_key = hashlib.sha256(b"TalebPoastingSouthernEuropean").digest()
    account = Account.from_key(private_key)
    deployer_address = account.address
    
    set_balance(web3, deployer_address, Web3.to_wei(1, 'ether'))

    # NOTE: need to run `forge build` first
    # The compiled contract is expected at compiled/Oracle.sol/PriceOracle.json
    contract_info = json.loads(Path("compiled/Oracle.sol/PriceOracle.json").read_text())
    abi = contract_info["abi"]
    bytecode = contract_info["bytecode"]["object"]

    contract = web3.eth.contract(abi=abi, bytecode=bytecode)

    construct_txn = contract.constructor().build_transaction(
        {
            "from": deployer_address,
            "nonce": web3.eth.get_transaction_count(deployer_address),
        }
    )

    tx_create = web3.eth.account.sign_transaction(construct_txn, account.key)
    tx_hash = web3.eth.send_raw_transaction(tx_create.raw_transaction)

    rcpt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Oracle deployed at: {rcpt.contractAddress}")
    return rcpt.contractAddress


def deploy(web3: Web3, deployer_address: str, deployer_privateKey: str, player_address: str) -> str:
    predeploy(web3)
    uri = web3.provider.endpoint_uri
    contract_info = json.loads(Path("compiled/Setup.sol/Setup.json").read_text())
    abi = contract_info["abi"]
    bytecode = contract_info["bytecode"]["object"]

    contract = web3.eth.contract(abi=abi, bytecode=bytecode)

    construct_txn = contract.constructor().build_transaction(
        {
            "from": deployer_address,
            "nonce": web3.eth.get_transaction_count(deployer_address),
            
        }
    )

    tx_create = web3.eth.account.sign_transaction(construct_txn, deployer_privateKey)
    tx_hash = web3.eth.send_raw_transaction(tx_create.raw_transaction)

    rcpt = web3.eth.wait_for_transaction_receipt(tx_hash)

    set_balance(web3, player_address, Web3.to_wei(100, 'ether'))

    return rcpt.contractAddress

app = sandbox.run_launcher(deploy)