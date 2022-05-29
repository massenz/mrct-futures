#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.
import time
import unittest

from tests.base import TestBase
from utils import get_env
from w3utils import (
    get_contract,
    new_transaction,
    sign_send_tx,
)

ONE_MONTH = 30 * 24 * 3600


class TestFactory(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.contract = self.contract_addr['SettlementFactory']
        self.owner = get_env('TEST_OWNER')
        self.key = get_env('TEST_KEY')

    def test_exists(self):
        factory = get_contract(self.w3, self.contract, "SettlementFactory")
        self.assertIsNotNone(factory)

    def test_create_settlement(self):
        factory = get_contract(self.w3, self.contract, "SettlementFactory")
        settlements = factory.functions.count().call()
        tx = factory.functions.newSettlement(
            'something', int(time.time() + ONE_MONTH), 200,  # Bob needs to hedge something a
                                                             # month from now
            get_env('bob'),                                  # Bob buys the future
            get_env('alice')                                 # Alice sells it to Bob
        ).buildTransaction(new_transaction(self.w3, self.owner))
        sign_send_tx(self.w3, tx, self.key)
        self.assertEqual(settlements + 1, factory.functions.count().call())
