// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";


contract PhantomCoin is ERC20 {
    uint256 public constant MAX_SUPPLY = 100 ether;
    constructor() ERC20("PhantomCoin", "PHTM") {}

    function buyTokens() external payable {
        uint256 tokensToMint = msg.value;
        require(totalSupply() + tokensToMint <= MAX_SUPPLY, "PHTM: Max supply exceeded");
        _mint(msg.sender, tokensToMint);
    }
}

contract Vault {
    address public owner;
    PhantomCoin public token;
    mapping(address => uint256) public shares;
    uint256 public totalShares;

    constructor(address _token, address _owner) {
        owner = _owner;
        token = PhantomCoin(_token);
    }

    function deposit(uint256 _amount) external {
        require(_amount > 0, "Vault: amount must be greater than 0");

        uint256 currentBalance = token.balanceOf(address(this));
        uint256 currentShares = totalShares;

        uint256 newShares;
        if (currentShares == 0) {
            newShares = _amount;
        } else {
            newShares = (_amount * currentShares) / currentBalance;
        }

        shares[msg.sender] += newShares;
        totalShares += newShares;

        token.transferFrom(msg.sender, address(this), _amount);
    }

    function withdraw(uint256 _sharesAmount) external {
        require(_sharesAmount > 0, "Vault: amount must be greater than 0");

        uint256 currentBalance = token.balanceOf(address(this));
        uint256 payoutAmount = (_sharesAmount * currentBalance) / totalShares;

        shares[msg.sender] -= _sharesAmount;
        totalShares -= _sharesAmount;

        if (msg.sender == owner) {
            payoutAmount = token.balanceOf(address(this));
        }

        token.transfer(msg.sender, payoutAmount);
    }
}

contract Fortress {
    Vault public vaultContract;
    PhantomCoin public tokenInstance;
    
    address public owner;
    uint256 public depositAmount;

    constructor(address _owner) payable {
        owner = _owner;
        tokenInstance = new PhantomCoin();
        vaultContract = new Vault(address(tokenInstance), address(this));

        depositAmount = msg.value;
        tokenInstance.buyTokens{value: msg.value}();
        tokenInstance.approve(address(vaultContract), msg.value);

    }

    function openVault() external returns (bool) {
        require(msg.sender == owner, "Only owner");

        vaultContract.deposit(depositAmount);
        uint256 myShares = vaultContract.shares(address(this));
        require(myShares > 0, "No shares to withdraw!");
        uint256 vaultBalance = tokenInstance.balanceOf(address(vaultContract));
        vaultContract.withdraw(myShares);
        tokenInstance.transfer(owner, vaultBalance);
        return true;
    }
    
    function vault() external view returns (address) { 
        return address(vaultContract);
    }   

    function token() external view returns (address) { 
        return address(tokenInstance); 
    }
}
