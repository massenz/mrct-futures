#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.
import time

from tests.base import TestBase
from utils import get_env
from w3utils import (
    get_contract,
    new_transaction,
    sign_send_tx,
)

FUTURES_DEX = 'FuturesDex'
ONE_MONTH = 30 * 24 * 3600


class TestFuturesDex(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.contract = get_contract(self.w3, self.contract_addr['DEX'], FUTURES_DEX)

    def test_exists(self):
        self.assertIsNotNone(self.contract)

    def test_create_settlement(self):
        settlements = self.contract.functions.count().call()
        tx = self.contract.functions.createFuture(
            'MSFT', int(time.time() + ONE_MONTH),  # Bob needs to hedge MSFT a month from now
            200,
            get_env('bob'),                        # Bob buys the future
            get_env('alice')                       # Alice sells it to Bob
        ).build_transaction(new_transaction(self.w3, self.owner))
        sign_send_tx(self.w3, tx, self.pk)
        self.assertEqual(settlements + 1, self.contract.functions.count().call())
