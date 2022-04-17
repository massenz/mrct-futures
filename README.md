# Creating an ERC20 Token

*Created by M. Massenzio, 2022-04-15*

# Concepts

A `Smart Contract` is a program that runs on the ETH B/c, a collection of code/data that resides at a specific address; it is a type of `Account`, so it can send transactions over the network and has a balance.

An `account` is an entity with an ETH balance: it can

* receive,
* hold, and
* send

ETH and `Tokens`.

> Transactions from an external account to a contract account can trigger code which can execute many different actions, such as transferring tokens or even creating a new contract

Contract accounts have a 42 hex address (168 bits): it gets generated from the creator's address and their `nonce`.

Accounts have four fields:

* `nonce`
* `balance`
* `codeHash`
* `storageRoot` (or 'storage hash')


### Keys

An `Account` is protected by a `Private Key` which is made up of 64 hex characters (256 bits) and can be encrypted with a password.

`Public Key` is generated with an EC signature algorithm (Keccak-256), last 20 bytes.


## Setup

Setting up the dev env with [REMIX](https://remix.ethereum.org/) and creating the first token: see the [Token.sol](token.sol) source.

```typescript

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

```

For local development we use [Hardhat](https://hardhat.org/):

1. installed the latest [Node.js](https://nodejs.org) LTS via `nvm`

```
└─( nvm install 16.14.2

└─( node --version
v16.14.2

```

2. Install Hardhat

```
└─( npm init      

└─( npm install --save-dev hardhat
```

3. Initialize project with Hardhat

```
└─( npx hardhat
```

**TODO**
> Audit finds many vulnerabilities, some `high`: fix them

## Alchemy & MATIC

Created an account with [Alchemy](https://dashboard.alchemyapi.io/) and created my first app (`MarcoToken`), and configured to use the Mumbai Polygon network.

The API App key and the Metamask Wallet account have been saved in the `.env` file (added to `.gitignore`):

```
npm install dotenv
touch .env
echo ".env" >> .gitignore
vim .env
```

[Polygon](https://faucet.polygon.technology/) can be used to issue test tokens (`MATIC`) to use to deploy the `MarcoToken` (use your Wallet address, from Metamask).

Remember to enable test networks and to add Polygon Mumbai to the Metamask extension (using [Chainlist](https://chainlist.org/)).


## Code

Added support for OpenZeppelin:

    npm install @openzeppelin/contracts

and added `Token.sol` to be deployed via `deploy.js`.

Hardhat provides some basic functionality:

```shell
npx hardhat accounts
npx hardhat compile
npx hardhat clean
npx hardhat test
npx hardhat node
node scripts/sample-script.js
npx hardhat help
```

Used `npx hardhat compile` to compile my `contracts` to `artifacts`, and then deploy with the `deploy.js` script:

```
└─( npx hardhat run ./scripts/deploy.js --network mumbai
Token deployed to: 0x3ec2C1426A615F3bD59Ca31203657bc9E2e53d18
```



## References


- [How to Create and Deploy an ERC20 Token – In 20 minutes](https://vitto.cc/how-to-create-and-deploy-an-erc20-token-in-20-minutes/)

- [ERC20 Token standard](https://ethereum.org/en/developers/docs/standards/tokens/erc-20/) and [API Documentation](https://docs.openzeppelin.com/contracts/4.x/api/token/erc20)

- [Smart Contracts](https://ethereum.org/en/developers/docs/smart-contracts/)

- [Ethereum Accounts](https://ethereum.org/en/developers/docs/accounts/)

- [Build Sandbox](https://sandbox.eth.build/)
