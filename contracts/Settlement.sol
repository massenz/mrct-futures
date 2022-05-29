// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract SettlementContract is Ownable {

    // Settlement into the Contract
    struct Settlement {
        // The name of the asset being settled.
        string asset;
        // The agreed-upon settlement value in MRCTs
        uint256 value;
        // The timestamp (seconds from Unix epoch) when this contract
        // must be settled by, or will expire.
        uint256 expires;
    }

    address payable public seller;
    address payable public buyer;
    Settlement settlement;

    constructor(string memory asset_, uint256 settlesAt_, uint256 value_,
        address payable buyer_, address payable seller_) {
        settlement = Settlement({
            asset : asset_,
            value : value_,
            expires : settlesAt_
        });
        seller = seller_;
        buyer = buyer_;
    }

    function settle() public payable {
        require(msg.sender == buyer, "Settlement: Buyer pays");
        require(msg.value == settlement.value, "Settlement: must settle for the contract value");
        // TODO: how do you transfer MRCTs here from the buyer to the seller?
    }
}
