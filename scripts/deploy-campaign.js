/*
 * Copyright (c) M. Massenzio, 2022.
 * All rights reserved.
 */

const hre = require("hardhat");

/**
 * Deploys the MarcoToken to the Ether blockchain.
 * @returns {Promise<void>}
 */
async function main() {
    const Campaign = await hre.ethers.getContractFactory("Campaign");
    const token = await Campaign.deploy(100);

    const result = {
        "Campaign": token.address,
    };
    console.log(JSON.stringify(result));
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
