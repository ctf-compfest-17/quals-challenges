// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

import "forge-std/Script.sol";

interface ISIAK3 {
    function NPM() external view returns (string memory);
    function UKT_AMOUNT() external view returns (uint256);
    function CURRENT_SEMESTER() external view returns (string memory);
    function payTuition(uint8 v, bytes32 r, bytes32 s, string calldata semester) external payable;
}

interface ISetup {
    function challenge() external view returns (address);
}

contract Solve is Script {
    uint256 constant RECOVERED_BOB_PRIVKEY = 0xa4e8e4e8cafea0b69e4d1de7f98f5e159f07728f056a6405e68f2aa0b5607219;

    address constant SETUP_CONTRACT_ADDR = 0xE1c19a8E8991b21E39C200F0598312E888629dF4;

    function run() external {
        uint256 playerPrivateKey = vm.envUint("PRIVKEY");

        ISetup setup = ISetup(SETUP_CONTRACT_ADDR);
        ISIAK3 challenge = ISIAK3(setup.challenge());

        string memory npm = challenge.NPM();
        uint256 uktAmount = challenge.UKT_AMOUNT();
        string memory targetSemester = challenge.CURRENT_SEMESTER();

        bytes32 messageHash = keccak256(abi.encodePacked(npm, uktAmount, targetSemester));

        (uint8 v, bytes32 r, bytes32 s) = vm.sign(RECOVERED_BOB_PRIVKEY, messageHash);

        vm.startBroadcast(playerPrivateKey);

        challenge.payTuition{value: uktAmount}(v, r, s, targetSemester);

        vm.stopBroadcast();
    }
}
