import json
import web3.eth
from web3 import Web3

ARTIFACTS = 'artifacts/contracts'


def get_env(key, envloc=".env", is_hex=True):
    with open(envloc) as env:
        for line in env.readlines():
            if line.startswith(key):
                pk = line.split("=")[1].replace('"', '').strip()
                if is_hex and not pk.startswith('0x'):
                    pk = '0x' + pk
                return pk
    raise KeyError(f"{key} not found in {envloc}")


def tokens_from_willies(willies, decimals):
    return willies / (10 ** decimals)


def get_abi(artifact):
    loc = '/'.join([ARTIFACTS, artifact])
    if not loc.endswith('.json'):
        loc += '.json'
    with open(loc) as c:
        return json.load(c).get('abi')


def new_transaction(w3conn, owner, gas=200000):
    return {
        'from': owner,
        'nonce': w3conn.eth.getTransactionCount(owner),
        'gas': gas,
        'gasPrice': w3conn.eth.gasPrice
    }


def get_web3_conn():
    provider = Web3.HTTPProvider(get_env('API_URL', is_hex=False))
    if not provider.isConnected():
        raise RuntimeError("Cannot connect")
    return Web3(provider)


def get_contract(w3conn):
    abi = get_abi('Token.sol/MarcoToken')
    return w3conn.eth.contract(address=get_env('CONTRACT_ADDRESS'), abi=abi)


def sign_send_tx(w3conn, tx):
    # Sign the transaction
    pk = get_env("PRIVATE_KEY")
    signed_tx = web3.eth.Account.signTransaction(tx, pk)
    tx_hash = w3conn.eth.send_raw_transaction(signed_tx.rawTransaction)
    w3conn.eth.wait_for_transaction_receipt(tx_hash)


def main(owner, recipient):
    w3conn = get_web3_conn()
    contract = get_contract(w3conn)
    symbol = contract.functions.symbol().call()
    decimals = contract.functions.decimals().call()
    total_supply = contract.functions.totalSupply().call()
    print(f"Total Supply: {tokens_from_willies(total_supply, decimals)} {symbol}")

    balance = contract.functions.balanceOf(owner).call()
    print(f"Contract Owner balance: {tokens_from_willies(balance, decimals)} {symbol}")

    # Send tokens to `recipient` from the `owner`
    #
    # As MRCT has 6 decimals, 100,000 willies (10^5) is 0.1 MRCT
    tx = contract.functions.transfer(recipient, 100000).buildTransaction(new_transaction(w3conn, owner))
    sign_send_tx(w3conn, tx)

    # Confirm that the transfer was successful
    balance = contract.functions.balanceOf(recipient).call()
    print(f"Marco Balance: {tokens_from_willies(balance, decimals)} {symbol}")

    # The `owner` (and only they) can issue new tokens (here, 0.20 MRCTs)
    tx = contract.functions.issueTokens(20000).buildTransaction(new_transaction(w3conn, owner))
    sign_send_tx(w3conn, tx)

    # Confirm the new supply is in place
    total_supply = contract.functions.totalSupply().call()
    print(f"Total Supply: {tokens_from_willies(total_supply, decimals)} {symbol}")


if __name__ == '__main__':
    main(owner=get_env('WALLET'), recipient=get_env('OTHER_WALLET'))
