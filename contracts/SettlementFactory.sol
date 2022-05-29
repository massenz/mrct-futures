// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./Settlement.sol";

contract SettlementFactory is Ownable {
    SettlementContract[] private _futures;

    function count() public view returns (uint256) {
        return _futures.length;
    }

    function newSettlement(
        string memory asset_,
        uint256 settlesAt_,
        uint256 value_,
        address payable buyer_,
        address payable seller_
    ) public returns(uint256) {
        SettlementContract future = new SettlementContract(
            asset_, settlesAt_, value_, buyer_, seller_);
        _futures.push(future);
        emit FutureCreated(future);
        return count();
    }

    event FutureCreated(SettlementContract future);
}
