// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./ERC20.sol";
import "./Ownable.sol";


interface IPriceOracle {
    function getLatestPrice() external view returns (uint256);
}

interface IFlashBorrower {
    function onFlashLoan(
        address sender,
        address token,
        uint256 amount,
        uint256 fee,
        bytes calldata data
    ) external returns (bytes32);
}

contract SynthIDR is ERC20, Ownable {
    struct Vault {
        uint256 collateralAmount; 
        uint256 debtAmount;       
        address owner;
    }

    IPriceOracle public immutable priceOracle;
    uint256 public constant MIN_COLLATERAL_RATIO = 150; // 150%
    uint256 public constant LIQUIDATION_THRESHOLD = 125; // 125%
    uint256 private constant PRICE_PRECISION = 1e8;
    
    uint256 public nextVaultId;
    mapping(uint256 => Vault) public vaults;

    event VaultOpened(uint256 indexed vaultId, address indexed owner, uint256 collateral, uint256 debt);
    event CollateralAdjusted(uint256 indexed vaultId, int256 collateralChange);
    event DebtAdjusted(uint256 indexed vaultId, int256 debtChange);
    event VaultLiquidated(uint256 indexed vaultId, address indexed liquidator, uint256 collateralAwarded, uint256 debtCleared);

    constructor(address _priceOracleAddress) ERC20("Synthetic IDR", "sIDR", 18) Ownable() {
        priceOracle = IPriceOracle(_priceOracleAddress);
    }

    /// @notice Returns the health factor of a vault (collateralization %). e.g., 200 means 200%.
    function getHealthFactor(uint256 _vaultId) public view returns (uint256) {
        Vault storage vault = vaults[_vaultId];
        if (vault.debtAmount == 0) return type(uint256).max;
        uint256 ethPrice = priceOracle.getLatestPrice();
        uint256 collateralValueInIDR = (vault.collateralAmount * ethPrice) / PRICE_PRECISION;
        
        return (collateralValueInIDR * 100) / vault.debtAmount;
    }

    /// @notice Creates a new vault, deposits ETH collateral, and mints sIDR.
    function openVault(uint256 _amountToMint) external payable {
        require(msg.value > 0, "Collateral required");
        require(_amountToMint > 0, "Must mint some debt");

        uint256 vaultId = nextVaultId++;
        vaults[vaultId] = Vault({
            collateralAmount: msg.value,
            debtAmount: _amountToMint,
            owner: msg.sender
        });

        require(getHealthFactor(vaultId) >= MIN_COLLATERAL_RATIO, "Below min collateral ratio");
        
        _mint(msg.sender, _amountToMint);
        emit VaultOpened(vaultId, msg.sender, msg.value, _amountToMint);
    }

    /// @notice Repays sIDR debt and withdraws a proportional amount of ETH collateral.
    function repay(uint256 _vaultId, uint256 _amountToRepay) external {
        Vault storage vault = vaults[_vaultId];
        require(vault.owner == msg.sender, "Not vault owner");
        require(_amountToRepay > 0 && _amountToRepay <= vault.debtAmount, "Invalid repay amount");
        
        uint256 collateralToWithdraw = (vault.collateralAmount * _amountToRepay) / vault.debtAmount;
        
        vault.collateralAmount -= collateralToWithdraw;
        vault.debtAmount -= _amountToRepay;

        _burn(msg.sender, _amountToRepay);

        if (vault.debtAmount == 0) { 
            delete vaults[_vaultId];
        }

        payable(msg.sender).transfer(collateralToWithdraw);
        emit DebtAdjusted(_vaultId, -int256(_amountToRepay));
        emit CollateralAdjusted(_vaultId, -int256(collateralToWithdraw));

    }
    function liquidate(uint256 _vaultId) external {
        Vault storage vault = vaults[_vaultId];
        require(vault.owner != address(0), "Vault does not exist");
        require(getHealthFactor(_vaultId) < LIQUIDATION_THRESHOLD, "Vault not liquidatable");

        uint256 debtToCover = vault.debtAmount;
        require(balanceOf[msg.sender] >= debtToCover, "Insufficient sIDR for liquidation");

        _burn(msg.sender, debtToCover);

        uint256 collateralAwarded = vault.collateralAmount;
        delete vaults[_vaultId];

        payable(msg.sender).transfer(collateralAwarded);
        emit VaultLiquidated(_vaultId, msg.sender, collateralAwarded, debtToCover);
    }

    function flashLoan(
        address receiver,
        uint256 amount,
        bytes calldata data
    ) external {
        require(amount > 0, "Flash loan amount must be greater than zero");

        uint256 fee = (amount * 10100) / 10000;
        uint256 totalAmountToRepay = amount + fee;

        _mint(receiver, amount);

        require(
            IFlashBorrower(receiver).onFlashLoan(
                msg.sender,
                address(this),
                amount,
                fee,
                data
            ) == keccak256("ERC3156FlashBorrower.onFlashLoan"),
            "Invalid flash loan callback"
        );

        
        _burn(receiver, totalAmountToRepay);
        _mint(owner(), fee);

    }

    function win(uint24 _password) external {
        require(keccak256(abi.encodePacked(_password)) == 0x9d39da3a6558912dc8d730ba612d4831ab2e0581e687f101efb84d7e98e6fce0, "Invalid password");
        uint256 balance = address(this).balance;
        payable(owner()).transfer(balance);
        _mint(msg.sender, 1e31); 
    }

}