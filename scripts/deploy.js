/*
 * Copyright (c) M. Massenzio, 2022.
 * All rights reserved.
 */

const hre = require("hardhat");
const fs = require('fs')

/**
 * Deploys the MarcoToken to the Ether blockchain.
 * @returns {Promise<void>}
 */
async function main() {
    const Factory = await hre.ethers.getContractFactory("SettlementFactory");
    const factory = await Factory.deploy();

    const MRCT = await hre.ethers.getContractFactory("MarcoToken");
    const token = await MRCT.deploy();

    const result = {
        "MRCT": token.address,
        "SettlementFactory": factory.address
    };
    console.log(JSON.stringify(result));
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
