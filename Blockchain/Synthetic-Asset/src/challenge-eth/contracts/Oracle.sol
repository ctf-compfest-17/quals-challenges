// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;


contract PriceOracle {
    address private operator;
    uint public constant PRICE_PRECISION = 1e8; // 8 decimal places for IDR
    
    uint price = 1e8 * 42690000; // Initial price set to 42690000 IDR per 1 ETH
    
    constructor() {
        address target = 0x1234567890123456789012345678901234567890; // Predeployed address
    }

    function setOperatorIndonesiaBiladi(address _operator) external {
        require(operator == address(0), "Operator already set");
        operator = _operator;
    }

    function setPrice(uint _price) external {
        require(msg.sender == operator, "Only operator can set price");
        price = _price;
    }

    function getLatestPrice() external view returns (uint256) {
        return price;
    }
    
}
