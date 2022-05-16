#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.
import web3

from w3utils import (
    get_abi,
    get_web3_conn,
    new_transaction,
    sign_send_tx,
    tokens_from_units,
)


def get_contract(w3conn: web3.Web3, address: str) -> web3.eth.Contract:
    abi = get_abi('Token', 'MarcoToken')
    return w3conn.eth.contract(address=address, abi=abi)


def mint(address: str, amount: float, owner: str, pk: str, network='LOCAL_URL') -> float:
    """Request to mint `amount` tokens from the contract, signed by the `owner`

    :param address: the contract's address
    :param amount: the number of tokens to mint
    :param owner: the owner of the contract (assuming it's an Ownable one)
    :param pk: the Private Key of the `owner`
    :param network: a URL to connect to an L2 network for further dispatch to a Blockchain
    :return: the resulting total supply in base units (Willies) which are a `10^decimals` fraction
            of tokens (one millionth, when `decimals` is 6)
    """
    w3conn = get_web3_conn(network)
    contract = get_contract(w3conn, address)
    symbol = contract.functions.symbol().call()
    decimals = contract.functions.decimals().call()

    # The `owner` (and only they) can mint new tokens
    tx = contract.functions.issueTokens(amount).buildTransaction(new_transaction(w3conn, owner))
    sign_send_tx(w3conn, tx, pk)

    # Confirm the new supply is in place
    total_supply = contract.functions.totalSupply().call()
    print(f"Total Supply: {tokens_from_units(total_supply, decimals)} {symbol}")
    return total_supply
