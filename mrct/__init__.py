#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.
#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.

"""
This package manages the MCRT (MarcoToken) DAO Contract.

The contract provides facilities to settle physical contracts (which are represented by NFTs -
ERC721) via an ERC20 contract.

See `contracts/MRCT.sol` for more details.
"""
from eth_account import Account
from eth_account.signers.local import LocalAccount

from utils import get_env
from w3utils import (
    w3_conn,
    new_transaction,
    sign_send_tx,
    get_contract,
)


class MRCT(object):
    def __init__(self, address: str = None, private_key: str = None, url: str = None):
        """Creates a new MRCT class to manage the ERC20 contract

        Uses value from the "dot env" (`.env`) configuration file, unless overridden here.

        :param address: the Web3 address for the contract (or CONTRACT_ADDRESS)
        :param private_key: the contract's Owner Private Key (or PRIVATE_KEY)
        :param network: the network to connect to, as a URL (uses API_URL if not specified)
        :return: the newly configured MRCT to connect to the contract
        """
        self.owner: LocalAccount = Account.from_key(private_key or get_env('PRIVATE_KEY'))
        self.contract_address = address or get_env('CONTRACT_ADDRESS')
        self.w3 = w3_conn(url or get_env('API_URL'))
        self.contract = get_contract(self.w3, self.contract_address, "MarcoToken")

    @property
    def decimals(self):
        return self.contract.functions.decimals().call()

    @property
    def symbol(self):
        return self.contract.functions.symbol().call()

    @property
    def total_supply(self):
        total_supply = self.contract.functions.totalSupply().call()
        return total_supply

    def mint(self, amount: float) -> float:
        """Request to mint `amount` tokens from the contract, signed by the `owner`

        @param amount: the number of tokens to mint
        @return the resulting total supply in base units (Willies) which are a `10^decimals`
                fraction of tokens (one millionth, when `decimals` is 6)
        """
        tx = self.contract.functions.issueTokens(amount).build_transaction(
            new_transaction(self.w3, self.owner.address))
        sign_send_tx(self.w3, tx, self.owner.key)

        # Confirm the new supply is in place
        return self.total_supply

    def send(self, recipient: LocalAccount, amount: int) -> float:
        """Sends to `recipient` `amount` MRCT tokens """
        # Send tokens to `recipient` from the `owner`
        tx = self.contract.functions.transfer(recipient.address, amount).build_transaction(
             new_transaction(self.w3, self.w3.toHex(self.owner.key)))
        sign_send_tx(self.w3, tx, self.owner.key)

        # Confirm that the transfer was successful
        balance = self.contract.functions.balanceOf(recipient).call()
        return balance
