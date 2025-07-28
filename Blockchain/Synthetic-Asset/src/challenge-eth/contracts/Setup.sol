// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./SynthIDR.sol";
import "./Oracle.sol";


contract Setup {
    SynthIDR public challenge;

    constructor() payable {
        challenge = new SynthIDR(
            address(0xc256638034612C1a13a37cF0254967AEB902404E) // Predeployed
        );   
    }

    function isSolved() external view returns (bool) {
        // Check if the contract has a non-zero balance of sIDR
        return challenge.balanceOf(address(this)) > 1e32; 
    }
}
