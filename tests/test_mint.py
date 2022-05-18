#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.

from base import TestBase
from mrct import MRCT
from utils import get_env
from w3utils import tokens_from_units


class TestContract(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.owner = get_env('TEST_OWNER')
        self.pk = get_env('TEST_KEY')
        self.assertIsNotNone(self.contract_addr)
        self.mrct = MRCT(address=self.contract_addr, private_key=self.pk, url=get_env('LOCAL_URL'))

    def test_can_mint(self):
        willies = self.mrct.mint(100)
        self.assertEqual(100, tokens_from_units(willies, 6))

    def test_mint_increase_owner_balance(self):
        balance = self.mrct.contract.functions.balanceOf(self.owner).call()
        increase = 225
        self.mrct.mint(increase)
        new_balance = self.mrct.contract.functions.balanceOf(self.owner).call()
        self.assertAlmostEqual(new_balance, balance + increase * 10**6)

