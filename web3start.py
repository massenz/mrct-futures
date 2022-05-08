#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.


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


def main(owner, recipient):
    w3conn = get_web3_conn()
    contract = get_contract(w3conn)
    symbol = contract.functions.symbol().call()
    decimals = contract.functions.decimals().call()
    total_supply = contract.functions.totalSupply().call()
    print(f"Total Supply: {tokens_from_units(total_supply, decimals)} {symbol}")

    balance = contract.functions.balanceOf(owner).call()
    print(f"Contract Owner balance: {tokens_from_units(balance, decimals)} {symbol}")

    # Send tokens to `recipient` from the `owner`
    #
    # As MRCT has 6 decimals, 100,000 willies (10^5) is 0.1 MRCT
    tx = contract.functions.transfer(recipient, 100000).buildTransaction(new_transaction(w3conn, owner))
    sign_send_tx(w3conn, tx)

    # Confirm that the transfer was successful
    balance = contract.functions.balanceOf(recipient).call()
    print(f"Recipient's Balance: {tokens_from_units(balance, decimals)} {symbol}")

    # The `owner` (and only they) can issue new tokens (here, 0.20 MRCTs)
    tx = contract.functions.issueTokens(20000).buildTransaction(new_transaction(w3conn, owner))
    sign_send_tx(w3conn, tx)

    # Confirm the new supply is in place
    total_supply = contract.functions.totalSupply().call()
    print(f"Total Supply: {tokens_from_units(total_supply, decimals)} {symbol}")


if __name__ == '__main__':
    main(owner=get_env('WALLET'), recipient=get_env('OTHER_WALLET'))
