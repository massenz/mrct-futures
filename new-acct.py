#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.

from web3 import Web3

w3 = Web3()
acc = w3.eth.account.create()
print(f'private key={w3.toHex(acc.key)}, account={acc.address}')
