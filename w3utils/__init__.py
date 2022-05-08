#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.
import json

from web3 import Web3
import web3.eth

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


def sign_send_tx(w3conn, tx):
    """Signs the transaction and sends it to the ETH blockchain"""
    pk = get_env("PRIVATE_KEY")
    signed_tx = web3.eth.Account.signTransaction(tx, pk)
    tx_hash = w3conn.eth.send_raw_transaction(signed_tx.rawTransaction)
    w3conn.eth.wait_for_transaction_receipt(tx_hash)


