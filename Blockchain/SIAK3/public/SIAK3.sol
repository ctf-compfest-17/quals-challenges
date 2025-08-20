// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract SIAK3 {
    address public constant STUDENT_ADDRESS = 0x6dc7C25252515164FF388e10bB6dD1f5501fc88e;
    string public constant NPM = "2206422922";
    uint256 public constant UKT_AMOUNT = 0.1 ether;

    mapping(string => bool) public paidSemesters;

    constructor() payable {}
    struct SemesterPayment {
        uint8 v;
        bytes32 r;
        bytes32 s;
        string semester;
    }
    mapping(uint256 => SemesterPayment) public Payments;
    uint256 public PaymentCount;

    event TuitionPaid(address indexed student, string semester);

    function payTuition(
        uint8 v,
        bytes32 r,
        bytes32 s,
        string calldata semester
    ) external payable {
        require(!paidSemesters[semester], "This semester has already been paid");
        require(msg.value >= UKT_AMOUNT, "Insufficient payment");
        
        bytes32 messageHash = keccak256(abi.encodePacked(NPM, UKT_AMOUNT, semester));
        bytes32 ethSignedHash = keccak256(
            abi.encodePacked("\x19Ethereum Signed Message:\n32", messageHash)
        );
        
        address signer = ecrecover(ethSignedHash, v, r, s);
        require(signer == STUDENT_ADDRESS, "Invalid signature");

        paidSemesters[semester] = true;

        Payments[PaymentCount] = SemesterPayment({
            v: v,
            r: r,
            s: s,
            semester: semester
        });
        PaymentCount++;

        emit TuitionPaid(signer, semester);
        
        if (msg.value > UKT_AMOUNT) {
            payable(msg.sender).transfer(msg.value - UKT_AMOUNT);
        }
    }
}
