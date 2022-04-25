// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Capped.sol";

contract MarcoToken is ERC20Capped, Ownable {

    // Specify the decimals: one Marco Token can be subdivided in 10^6
    // (one milion) Willies.
    function decimals() public view virtual override returns (uint8) {
      return 6;
    }

    constructor() ERC20("MarcoToken", "MRCT")
        ERC20Capped(1000000000) {
    }

    function issueTokens(uint tokens) public onlyOwner {
        _mint(msg.sender, tokens * 10^decimals());
        emit TokensMinted(tokens);
    }

    event TokensMinted(uint amount);
}
