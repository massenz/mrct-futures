#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.

from tests.base import TestBase
from utils import get_env


class TestAccounts(TestBase):
    def test_ganache_accounts(self):
        pairs = TestAccounts.keys_from_mnemonic(get_env('MNEMONIC', is_hex=False))
        self.assertEqual(
            pairs[0], (get_env('TEST_OWNER'), get_env('TEST_KEY')))
        self.assertEqual(
            pairs[3], (get_env('alice'), get_env('alice_pk')))
        self.assertEqual(
            pairs[7], (get_env('bob'), get_env('bob_pk')))
