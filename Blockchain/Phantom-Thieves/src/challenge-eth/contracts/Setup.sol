// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Fortress.sol";

contract Setup {
    Fortress public challenge;

    constructor() payable {
        challenge = new Fortress{value: 0.5 ether}(address(this));
    }

    function isSolved() external view returns (bool) {
        Vault vault = challenge.vaultContract();

        if (vault.totalShares() == 0) {
            return false;
        }
        uint256 _amount = challenge.tokenInstance().balanceOf(address(challenge));
        uint256 currentBalance = challenge.tokenInstance().balanceOf(address(vault));
        uint256 currentShares = vault.totalShares();
        uint256 shares = (_amount * currentShares) / currentBalance;

        return shares == 0;
    }
}
