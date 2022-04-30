// Created by Marco, 2022-04-13
//
// Hardhat deployment configuration.

require("@nomiclabs/hardhat-waffle");
require('dotenv').config()

// Secret values from .env file
const { API_URL, PRIVATE_KEY } = process.env

// You need to export an object to set up your config
// Go to https://hardhat.org/config/ to learn more
/**
 * @type import('hardhat/config').HardhatUserConfig
 */
module.exports = {
  solidity: "0.8.4",
  networks: {
    mumbai: {
      url: API_URL,
      accounts: [`0x${PRIVATE_KEY}`]
    }
  }
};

/**
 * A task to transfer funds to a wallet
 */
task("xfer", "Transfer funds to a wallet")
  .addParam("wallet", "The address of the wallet to transfer funds to")
  .addParam("amt", "The amount of willies (one millionth of a MarcoToken) to transfer", undefined, types.int)
  .setAction(async ({wallet, amt}) => {
    console.log("Wallet:", wallet, "- Amount:", amt);
    // TODO: how do we invoke transfer.js from here?
  })
