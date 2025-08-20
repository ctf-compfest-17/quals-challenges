# FILE: chal.py (FINAL, CORRECTED VERSION)
import json
from pathlib import Path
import sandbox
from web3 import Web3

BOB_PRIVKEY = "0xa4e8e4e8cafea0b69e4d1de7f98f5e159f07728f056a6405e68f2aa0b5607219"
BOB_ADDRESS = "0x6dc7C25252515164FF388e10bB6dD1f5501fc88e"

SIGNATURES_FOR_DEPLOYMENT = [
    (27, 0xcc01ccb300f10f031158676c41f6873354f95207c6e19fdce3a7f42af4d76691, 0x02131bd89e614118557b2ff6794c90cae20510a0f0f99e4845f484856b8e4c34, "2022-1"),
    (27, 0x97899d469d055b62c50d13443aee019f8028c1d577b665063062e841b57e8932, 0x7b25f224cb4a5ece59c9f28aaf13eb833e0256ba8461bad0889a2ca4ee0f8e7d, "2022-2"),
    (27, 0xf720ecb1dad6068cf8196023e744f3cc503f836c1f29e56b1752ee074c3c59ed, 0x7c0f98445465b4c3f320abb6238bc987ce065292c673402513af718509e4c174, "2023-1"),
    (28, 0xdfa3554e4ec008d16ab70d538bb4955fba2edf50c807a84b60899d274e505128, 0x0285b918d5a418be78af25e816e388fbe5051e207def0ef5ec033b05a4210e1a, "2023-2"),
    (28, 0x23aa99b4d580123537705c790c9e3f691e97c17c7113d0320cbd221734edacbe, 0x6d8cc9f8c2313f1a4be3c0e4abd79acff35708703e6833b2937f203bbd18d4bd, "2024-1"),
    (27, 0xe7f9f89fa9ea62e94d93e05ab85245a710fb703a1df224edd7afaf35977c60d0, 0xa7ac159403fa59d5ec5061a94095686d3ecffc1f77ba152402fb1d5615aea28a, "2024-2")
]

def set_balance(web3: Web3, account_address: str, amount_wei: int):
    web3.provider.make_request("anvil_setBalance", [account_address, hex(amount_wei)])

def deploy(web3: Web3, deployer_address: str, deployer_privateKey: str, player_address: str) -> str:
    setup_info = json.loads(Path("compiled/Setup.sol/Setup.json").read_text())
    siak3_info = json.loads(Path("compiled/SIAK3.sol/SIAK3.json").read_text())
    
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

    set_balance(web3, BOB_ADDRESS, Web3.to_wei(2, 'ether'))
    set_balance(web3, player_address, Web3.to_wei(2, 'ether'))

    # Simulate Bob past payments
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

def pre_tx_hook(data, node_info):
    """
    Executed before a transaction is processed.
    Returns:
        - status: HTTP status code (e.g., 200 for success, 400 for error)
        - msg: Message to be returned in the response in case of non 2xx status
    """
    return 200, ""

def post_tx_hook(data, response, node_info):
    
    """
    Executed after a transaction is processed.
    Returns:
        - status: HTTP status code (e.g., 200 for success, 400 for error)
        - msg: Message to be returned in the response in case of non 2xx status
    """
    return 200, ""

app = sandbox.run_launcher(
    deploy,
    pre_tx_hook=pre_tx_hook,
    post_tx_hook=post_tx_hook
)
