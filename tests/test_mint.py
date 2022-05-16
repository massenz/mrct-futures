#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.

import unittest

from base import TestBase
from scripts.mint import mint, get_contract
from utils import get_env
from w3utils import tokens_from_units, get_web3_conn


class TestContract(TestBase):
    def setUp(self) -> None:
        self.owner = get_env('TEST_OWNER')
        self.pk = get_env('TEST_KEY')

    def test_can_mint(self):
        self.assertIsNotNone(self.contract_addr)
        willies = mint(
            self.contract_addr,
            100,
            self.owner,
            self.pk)
        self.assertEqual(100, tokens_from_units(willies, 6))

    def test_mint_increase_owner_balance(self):
        contract = get_contract(get_web3_conn('LOCAL_URL'), self.contract_addr)
        balance = contract.functions.balanceOf(self.owner).call()
        increase = 225
        mint(
            self.contract_addr,
            increase,
            self.owner,
            self.pk)
        new_balance = contract.functions.balanceOf(self.owner).call()
        self.assertAlmostEqual(new_balance,
                               balance + increase * 10**6)

