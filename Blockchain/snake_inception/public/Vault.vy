# @version 0.2.16

event Claimed:
    user: indexed(address)
    amount: uint256

claimed: public(HashMap[bytes32, bool])
target_message: public(bytes32)
reward_amount: public(uint256)
CEO: public(address)

@external
def __init__():
    # The message players need to sign
    self.target_message = keccak256("I, The Compfest CEO, Hereby Declare That I Will Give 20 ETH To this person")
    self.reward_amount = 20 * 10**18  # 20 ETH
    self.CEO = 0xB1fdC7607932246c3551D4aA17e19c1eA95840F9  

@external
@payable
def fund_contract():
    """Owner can fund the contract"""
    pass

@external
@view
def get_message_to_sign() -> bytes32:
    """Returns the message hash players need to sign"""
    return self.target_message


@internal
@pure
def _recover_signer(message_hash: bytes32, v: uint256, r: uint256, s: uint256) -> address:
    """Recover the signer address from signature"""
    return ecrecover(message_hash, v, r, s)

@external
@nonreentrant("claim") 
def claim_reward(v: uint256, r: uint256, s: uint256):
    """Claim 20 ETH with valid signature"""
    
    temp: address = msg.sender
    assert temp.codesize == 0, "Human Only Vrooo..."
    
    sig_hash: bytes32 = keccak256(concat(convert(v, bytes32), convert(r, bytes32), convert(s, bytes32)))

    assert not self.claimed[sig_hash], "You Already Claimed Vrooo....d"
    
    signer: address = self._recover_signer(self.target_message, v, r, s)
    
    assert signer == self.CEO, "Invalid signature"
    
    raw_call(msg.sender, b"", value=self.reward_amount)
    
    self.claimed[sig_hash] = True

    log Claimed(msg.sender, self.reward_amount)

@external
@nonreentrant("claim") 
def gamble_reward(v: uint256, r: uint256, s: uint256):
    """Gamble 20 ETH with valid signature"""

    temp: address = msg.sender
    assert temp.codesize == 0, "Human Only Vrooo..."

    sig_hash: bytes32 = keccak256(concat(convert(v, bytes32), convert(r, bytes32), convert(s, bytes32)))

    assert not self.claimed[sig_hash], "You Already Claimed Vrooo....d"
    
    signer: address = self._recover_signer(self.target_message, v, r, s)
    
    assert signer == self.CEO, "Invalid signature"

    real_reward: uint256 = self.reward_amount * 2  # Double the reward for gambling

    if(convert(blockhash(block.number-1), uint256) % 2 == 0):
        # If the last byte of the block hash is even, the player wins
        raw_call(msg.sender, b"", value=real_reward)
    else:
        # If the last byte of the block hash is odd, the player loses
        # No ETH is sent, but the claim is still marked as used
        raw_call(msg.sender, b"lmao", value=0)
    
    self.claimed[sig_hash] = True

    log Claimed(msg.sender, self.reward_amount)


