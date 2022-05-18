#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.
from web3.auto import w3

from tests.base import TestBase
from utils import get_env
from w3utils import new_transaction, sign_send_tx, get_contract


class TestAccounts(TestBase):

    @classmethod
    def get_accounts(cls):
        return cls.keys_from_mnemonic(get_env('MNEMONIC'))

    def setUp(self) -> None:
        super().setUp()
        self.pairs = self.get_accounts()

    def test_ganache_accounts(self):
        self.assertEqual(
            self.pairs[0], (get_env('TEST_OWNER'), get_env('TEST_KEY')))
        self.assertEqual(
            self.pairs[3], (get_env('alice'), get_env('alice_pk')))
        self.assertEqual(
            self.pairs[7], (get_env('bob'), get_env('bob_pk')))

    def test_balance(self):
        # We leave the last account alone, so it should always have 100 ETH
        no_name = self.pairs[9]
        balance = self.w3.eth.get_balance(no_name[0])
        self.assertEqual(100, w3.fromWei(balance, 'ether'))

    def test_transfer(self):
        alice = self.pairs[3]
        bob = self.pairs[7]
        amount = 0.005
        balance = self.w3.eth.get_balance(bob[0])
        tx = new_transaction(self.w3, bob[0])
        tx['value'] = w3.toWei(amount, 'ether')
        tx['to'] = alice[0]
        sign_send_tx(self.w3, tx, bob[1])
        new_balance = self.w3.eth.get_balance(bob[0])
        self.assertAlmostEqual(amount, float(w3.fromWei(balance - new_balance, 'ether')),
                               places=3)

    def test_settle(self):
        bob = self.pairs[7]
        amount = 5
        balance = self.w3.eth.get_balance(bob[0])
        tx = new_transaction(
            self.w3, owner=bob[0], value=w3.toWei(amount, 'ether'))
        contract = get_contract(self.w3, self.contract_addr)
        tx = contract.functions.settle().buildTransaction(tx)
        sign_send_tx(self.w3, tx, bob[1])
        new_balance = self.w3.eth.get_balance(bob[0])
        self.assertAlmostEqual(amount, float(w3.fromWei(balance - new_balance, 'ether')),
                               places=1)
        self.assertEqual(amount, int(w3.fromWei(
            self.w3.eth.get_balance(self.contract_addr), 'ether')))
