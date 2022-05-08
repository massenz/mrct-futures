/*
 * Copyright (c) M. Massenzio, 2022.
 * All rights reserved.
 */

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
      accounts: [PRIVATE_KEY]
    }
  }
};
