#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.
import json

from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3
import web3.eth
from web3.auto import w3
from web3.middleware import construct_sign_and_send_raw_middleware

from utils import get_env

ARTIFACTS = 'artifacts/contracts'


def get_web3_conn():
    """Connects to the provider designated in the API_URL env var"""
    provider = Web3.HTTPProvider(get_env('API_URL', is_hex=False))
    if not provider.isConnected():
        raise RuntimeError("Cannot connect")
    return Web3(provider)


def tokens_from_units(units, decimals):
    return units / (10 ** decimals)


def get_abi(artifact):
    """Retrieves the ABI for the `artifact` (the Smart Contract)"""
    loc = '/'.join([ARTIFACTS, artifact])
    if not loc.endswith('.json'):
        loc += '.json'
    with open(loc) as c:
        return json.load(c).get('abi')


def new_transaction(w3conn, owner, gas=200000):
    """Creates a new dict to represent a Tx to be sent to the Contract"""
    return {
        'from': owner,
        'nonce': w3conn.eth.getTransactionCount(owner),
        'gas': gas,
        'gasPrice': w3conn.eth.gasPrice
    }


def sign_send_tx(w3conn, tx, pk):
    """Signs the transaction and sends it to the ETH blockchain"""
    # TODO: should be possible to create an Account from PK and then simply send Tx
    #   using:
    #       w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))
    signed_tx = web3.eth.Account.signTransaction(tx, pk)
    tx_hash = w3conn.eth.send_raw_transaction(signed_tx.rawTransaction)
    w3conn.eth.wait_for_transaction_receipt(tx_hash)


def wallet_addr(private_key):
    account: LocalAccount = Account.from_key(private_key)
    return account.address
