#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.
#
# Usage: send.py ACCT TOKENS

import sys

from utils import get_env
from w3utils import (
    get_abi,
    get_web3_conn,
    new_transaction,
    sign_send_tx,
    tokens_from_units,
)


def get_contract(w3conn):
    abi = get_abi('Token.sol/MarcoToken')
    return w3conn.eth.contract(address=get_env('CONTRACT_ADDRESS'), abi=abi)


def send(recipient, amount):
    w3conn = get_web3_conn()
    contract = get_contract(w3conn)
    owner = get_env('OWNER')

    # Send tokens to `recipient` from the `owner`
    tx = contract.functions.transfer(recipient, amount).buildTransaction(
         new_transaction(w3conn, owner))
    sign_send_tx(w3conn, tx, pk=get_env("PRIVATE_KEY"))

    # Confirm that the transfer was successful
    balance = contract.functions.balanceOf(recipient).call()
    print(f"Recipient's Balance: {tokens_from_units(balance, 6)} MRCT")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: send.py WALLET TOKENS")
        exit(1)
    send(sys.argv[1], int(sys.argv[2]))
