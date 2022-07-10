// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";


contract Future {
    // Settlement into the Contract
    struct Settlement {
        // The name of the asset being settled.
        string asset;
        // The agreed-upon settlement value in Wei
        uint price;
        // The timestamp (seconds from Unix epoch) when this contract
        // must be settled by, or will expire.
        uint expires;
    }

    address payable public seller;
    address payable public buyer;
    address payable private owner_;
    Settlement public settlement;
    bool public settled;
    bool private paid;

    constructor(string memory asset_, uint settlesAt_, uint eth_,
        address payable buyer_, address payable seller_) {
        settlement = Settlement({
            asset : asset_,
            price : eth_ * 10 ** 18,
            expires : settlesAt_
        });
        seller = seller_;
        buyer = buyer_;
        settled = false;
        paid = false;
        owner_ = payable(msg.sender);
    }

    function pay() public payable {
        require(paid == false, "Cannot pay contract fee twice");
        require(msg.sender == seller, "Only the Seller can pay the contract fees");
        require(msg.value >= 50000000 gwei, "Contract fees are .05 ETH");
        owner_.transfer(50000000 gwei);
        paid = true;
    }

    function settle() public payable {
        require(paid == true, "The Seller has not paid for the Future");
        require(settled == false, "Cannot settle the same contract twice");
        require(block.timestamp < settlement.expires, "Future expired");
        require(msg.sender == buyer, "Only the Buyer of this Settlement can buy the security");
        require(msg.value == settlement.price, "The paid amount must match the Settlement agreed price");
        seller.transfer(settlement.price);
        settled = true;
    }
}

contract FuturesDex is Ownable {
    address[] private futures_;

    function count() public view returns (uint256) {
        return futures_.length;
    }

    function createFuture(string memory asset_, uint settlesAt_, uint eth_,
            address payable buyer_, address payable seller_) public returns(uint) {

        // Explicitly convert the newly created contract to its address.
        address newFuture = address(
            new Future(asset_, settlesAt_, eth_, buyer_, seller_));
        futures_.push(newFuture);
        return count() - 1;
    }
}
