// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Capped.sol";

contract MarcoToken is ERC20Capped, Ownable {

    uint8 _dec = 6;

    // Specify the decimals: one Marco Token can be subdivided in 10^6
    // (one million) Willies.
    function decimals() public view virtual override returns (uint8) {
      return _dec;
    }

    // MarcoTokens are capped at 1,000 (10^9 Willies)
    constructor() ERC20("MarcoToken", "MRCT")
        ERC20Capped(1000000000) {
    }

    // Issues whole tokens (1M Willies)
    function issueTokens(uint tokens) public onlyOwner {
        uint willies =  tokens * 10**_dec;
        _mint(msg.sender, willies);
        emit TokensMinted(willies);
    }

    // Issues thousandths of tokens (`millies`)
    function issueMillies(uint millies) public onlyOwner {
        uint willies = millies * 10**(_dec - 3);
        _mint(msg.sender, willies);
        emit TokensMinted(willies);
    }

    event TokensMinted(uint amount);
}
