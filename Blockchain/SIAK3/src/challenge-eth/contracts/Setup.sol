// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

import "./SIAK3.sol";

contract Setup {
    SIAK3 public challenge;
    string public constant CURRENT_SEMESTER = "2025-1";

    constructor() payable {
        require(msg.value >= 1 ether, "Setup must be funded");
        challenge = new SIAK3{value: msg.value}();
    }

    function isSolved() external view returns (bool) {
        return challenge.paidSemesters(CURRENT_SEMESTER);
    }
}