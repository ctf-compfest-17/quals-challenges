// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Fortress.sol";

contract Setup {
    Fortress public challenge;

    constructor() payable {
        challenge = new Fortress{value: 0.5 ether}(address(this));
    }

    function isSolved() external view returns (bool) {
        return _isLocked();
    }

    function _isLocked() private view returns (bool) {
        Vault vault = challenge.vaultContract();

        if (vault.totalShares() == 0) {
            return false;
        }

        (bool success,) = address(challenge).staticcall(
            abi.encodeWithSignature("openVault()")
        );

        return !success;
    }
}