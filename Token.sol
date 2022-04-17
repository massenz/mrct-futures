// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Capped.sol";

contract MarcoToken is ERC20Capped, Ownable {

    // Specify the decimals: one Marco Token can be subdivided in 10^6
    // (one milion) Willies.
    uint TOKEN = 10**6;

    constructor(uint256 cap) ERC20("MarcoToken", "MRCT")
        ERC20Capped(cap) {
    }

    function issueTokens(uint tokens) public onlyOwner {
        _mint(msg.sender, tokens * TOKEN);
    }
}
