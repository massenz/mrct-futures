/* Copyright M. Massenzio (c) 2022
   Created 2022-04-29
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
