#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.
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


def mint(amount, owner, pk):
    w3conn = get_web3_conn()
    contract = get_contract(w3conn)
    symbol = contract.functions.symbol().call()
    decimals = contract.functions.decimals().call()
    total_supply = contract.functions.totalSupply().call()
    print(f"Total Supply: {tokens_from_units(total_supply, decimals)} {symbol}")

    balance = contract.functions.balanceOf(owner).call()
    print(f"Contract Owner balance: {tokens_from_units(balance, decimals)} {symbol}")

    # The `owner` (and only they) can mint new tokens
    tx = contract.functions.issueTokens(amount).buildTransaction(new_transaction(w3conn, owner))
    sign_send_tx(w3conn, tx, pk)

    # Confirm the new supply is in place
    total_supply = contract.functions.totalSupply().call()
    print(f"Total Supply: {tokens_from_units(total_supply, decimals)} {symbol}")
    balance = contract.functions.balanceOf(owner).call()
    print(f"Contract Owner balance: {tokens_from_units(balance, decimals)} {symbol}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: mint.py AMOUNT")
        exit(1)
    mint(amount=int(sys.argv[1]), owner=get_env('OWNER'), pk=get_env('PRIVATE_KEY'))
