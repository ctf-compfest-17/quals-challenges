// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract SIAK3 {
    address public constant STUDENT_ADDRESS = 0x6dc7C25252515164FF388e10bB6dD1f5501fc88e;
    string public constant NPM = "2206422922";
    uint256 public constant UKT_AMOUNT = 0.1 ether;
    string public constant CURRENT_SEMESTER = "2025-1";

    // YOUR SUGGESTION: A boolean state for every semester. Excellent!
    mapping(string => bool) public paidSemesters;

    constructor() payable {}
    // We still need to store the historical signatures for the attack.
    struct SemesterPayment {
        uint8 v;
        bytes32 r;
        bytes32 s;
        string semester;
    }
    mapping(uint256 => SemesterPayment) public pastPayments;
    uint256 public pastPaymentCount;

    event TuitionPaid(address indexed student, string semester);

    // The logic is now much cleaner.
    function payTuition(
        uint8 v,
        bytes32 r,
        bytes32 s,
        string calldata semester
    ) external payable {
        // 1. Check if this specific semester has already been paid.
        require(!paidSemesters[semester], "This semester has already been paid");
        require(msg.value >= UKT_AMOUNT, "Insufficient payment");
        
        // 2. Verify the signature (same as before).
        bytes32 messageHash = keccak256(abi.encodePacked(NPM, UKT_AMOUNT, semester));
        address signer = ecrecover(messageHash, v, r, s);
        require(signer == STUDENT_ADDRESS, "Invalid signature");

        // 3. Mark this semester as paid.
        paidSemesters[semester] = true;

        // 4. If it's a past semester, we still record its signature for the attack.
        if (keccak256(abi.encodePacked(semester)) != keccak256(abi.encodePacked(CURRENT_SEMESTER))) {
            pastPayments[pastPaymentCount] = SemesterPayment({
                v: v,
                r: r,
                s: s,
                semester: semester
            });
            pastPaymentCount++;
        }

        emit TuitionPaid(signer, semester);
        
        if (msg.value > UKT_AMOUNT) {
            payable(msg.sender).transfer(msg.value - UKT_AMOUNT);
        }
    }

    // A clean helper function to check the final win condition.
    function isChallengeSolved() public view returns (bool) {
        return paidSemesters[CURRENT_SEMESTER];
    }
}