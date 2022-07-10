// Copyright AlertAvert.com (c) 2022
// Created by M. Massenzio ()marco@alertavert.com) 2022-07-06
// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

contract Campaign {
    struct Request {
        string description;
        uint value;
        address payable recipient;
        bool complete;
        uint approvalCount;
        mapping(address => bool) approvals;
    }

    address public manager;
    uint public minimumContribution;
    mapping(address => bool) public approvers;
    mapping(uint => Request) public requests;
    uint numRequests;
    uint contributors;

    modifier restricted() {
        require(msg.sender == manager);
        _;
    }

    constructor (uint minimum) {
        manager = msg.sender;
        minimumContribution = minimum;
        numRequests = 0;
    }

    function contribute() public payable {
        require(msg.value > minimumContribution);
        approvers[msg.sender] = true;
        contributors++;
    }

    function createRequest(string memory description,
        uint value, address recipient) public restricted returns(uint){
        uint reqId = numRequests++;

        // Cannot create the request here as it contains a mapping.
        Request storage r = requests[reqId];
        r.description = description;
        r.value = value;
        r.recipient = payable(recipient);
        r.complete = false;
        r.approvalCount = 0;

        return reqId;
    }

    function approveRequest(uint index) public {
        Request storage request = requests[index];

        require(approvers[msg.sender]);
        require(!request.approvals[msg.sender]);

        request.approvals[msg.sender] = true;
        request.approvalCount++;
    }

    function finalizeRequest(uint index) public restricted {
        Request storage r = requests[index];

        require(!r.complete);
        require(r.approvalCount > (contributors / 2));

        r.recipient.transfer(r.value);
        r.complete = true;
    }
}
