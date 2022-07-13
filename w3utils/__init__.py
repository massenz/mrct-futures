#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.
import json
import os

import web3
import web3.eth
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3
from web3.auto import w3

ARTIFACTS = 'artifacts/contracts'


def w3_conn(url: str) -> Web3:
    """Connects to the provider designated in the API_URL env var"""
    provider = Web3.HTTPProvider(url)
    if not provider.isConnected():
        raise RuntimeError("Cannot connect")
    return Web3(provider)


def tokens_from_units(units: float, decimals: int) -> float:
    return units / (10 ** decimals)


def get_abi(solidity: str) -> dict:
    """Retrieves the ABI for the `artifact` (the Smart Contract)

    @param solidity: the name of the Solidity contract class which defines the contract
    @returns: a dict representing the contract's binary interface (ABI)
    """
    jsonfile = solidity + '.json'
    for dirpath, _, fnames in os.walk(ARTIFACTS):
        for name in fnames:
            if jsonfile == name:
                with open(os.path.join(dirpath, jsonfile)) as c:
                    return json.load(c).get('abi')


# TODO: add **kwargs
def new_transaction(w3conn: w3, owner: str, to: str = None, value: int = None, gas=2000000) -> \
        dict:
    """Creates a new dict to represent a Tx to be sent to the Contract"""
    tx = {
        'from': owner,
        'nonce': w3conn.eth.get_transaction_count(owner),
        'gas': gas,
        'gasPrice': w3conn.eth.gas_price
    }
    if to is not None:
        tx['to'] = to
    if value is not None:
        tx['value'] = value
    return tx


def sign_send_tx(w3conn: w3, tx: dict, pk: str):
    """Signs the transaction and sends it to the ETH blockchain"""
    # TODO: should be possible to create an Account from PK and then simply send Tx
    #   using:
    #       w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))
    signed_tx = web3.eth.Account.sign_transaction(tx, pk)
    tx_hash = w3conn.eth.send_raw_transaction(signed_tx.rawTransaction)
    return w3conn.eth.wait_for_transaction_receipt(tx_hash)


def wallet_addr(private_key: str) -> str:
    account: LocalAccount = Account.from_key(private_key)
    return account.address


def get_contract(w3conn: web3.Web3, address: str,
                 name: str = None, abi: dict = None) -> web3.eth.Contract:
    """Retrieves the Contract from its address and auto-discovers the ABI, if not provided

    :param w3conn: a valid connection to Web3
    :param address: the address of the contract
    :param name: the name of the contract definition, in Solidity; optional
    :param abi: the ABI of the contract's definition; optional, if not provided, it tries to
                locate it in the `ARTIFACTS` subtree.
    :return: the Web3 Contract
    """
    abi = abi or get_abi(name)
    return w3conn.eth.contract(address=address, abi=abi)
