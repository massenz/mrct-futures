/*
 * Copyright (c) M. Massenzio, 2022.
 * All rights reserved.
 */

const TokenName = "MarcoToken"
const hre = require("hardhat");

/**
 * Deploys the MarcoToken to the Ether blockchain.
 * @returns {Promise<void>}
 */
async function main() {
  const DevToken = await hre.ethers.getContractFactory(TokenName);
  const devToken = await DevToken.deploy();

  console.log("Contract deployed to:", devToken.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
