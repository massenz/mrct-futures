#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.
import json

import web3.eth
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3
from web3.auto import w3

from utils import get_env

ARTIFACTS = 'artifacts/contracts'


def get_web3_conn(url: str) -> Web3:
    """Connects to the provider designated in the API_URL env var"""
    provider = Web3.HTTPProvider(get_env(url, is_hex=False))
    if not provider.isConnected():
        raise RuntimeError("Cannot connect")
    return Web3(provider)


def tokens_from_units(units: float, decimals: int) -> float:
    return units / (10 ** decimals)


def get_abi(solidity: str, contract: str) -> dict:
    """Retrieves the ABI for the `artifact` (the Smart Contract)

    :param solidity: the name of the Solidity file which defines the contract(s), without .sol
    extension
    :param contract: the name of the Contract that we want the ABI of

    :returns: a dict representing the contract's binary interface (ABI)
    """
    if not solidity.endswith('.sol'):
        solidity += '.sol'
    loc = '/'.join([ARTIFACTS, solidity, contract])
    if not loc.endswith('.json'):
        loc += '.json'
    with open(loc) as c:
        return json.load(c).get('abi')


def new_transaction(w3conn: w3, owner: str, gas=200000) -> dict:
    """Creates a new dict to represent a Tx to be sent to the Contract"""
    return {
        'from': owner,
        'nonce': w3conn.eth.get_transaction_count(owner),
        'gas': gas,
        'gasPrice': w3conn.eth.gas_price
    }


def sign_send_tx(w3conn: w3, tx: dict, pk: str):
    """Signs the transaction and sends it to the ETH blockchain"""
    # TODO: should be possible to create an Account from PK and then simply send Tx
    #   using:
    #       w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))
    signed_tx = web3.eth.Account.sign_transaction(tx, pk)
    tx_hash = w3conn.eth.send_raw_transaction(signed_tx.rawTransaction)
    w3conn.eth.wait_for_transaction_receipt(tx_hash)


def wallet_addr(private_key: str) -> str:
    account: LocalAccount = Account.from_key(private_key)
    return account.address
