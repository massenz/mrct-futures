# Copyright AlertAvert.com (c) 2017. All rights reserved.
# Created by Marco Massenzio (marco@alertavert.com), 2017-09-03
import codecs
import os
import tempfile
import unittest

import web3
from eth_account import Account
from eth_account.hdaccount import ETHEREUM_DEFAULT_PATH
from eth_account.signers.local import LocalAccount

from utils import run_hh_script, get_env
from w3utils import w3_conn


def deploy_contract():
    print(f"Deploying contract from {os.getcwd()}")
    contract_addr = run_hh_script('deploy.js').strip()
    print(f"Contract address: {contract_addr}")
    return contract_addr


class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print(">>>> deploying contract")
        cls.contract_addr = deploy_contract()

    @staticmethod
    def temp_filename(suffix=None):
        """ Returns a temporary file."""
        filename = tempfile.mkstemp(suffix=suffix)[1]
        return filename

    @staticmethod
    def keys_from_mnemonic(mnemonic: str, num: int = 10) -> list[LocalAccount]:
        # TODO: this is not a "stable" API yet
        Account.enable_unaudited_hdwallet_features()
        keypairs = []
        for n in range(num):
            account_path = ETHEREUM_DEFAULT_PATH[:-1] + str(n)
            account = Account.from_mnemonic(mnemonic, account_path=account_path)
            keypairs.append((account.address, web3.Web3.toHex(account.key)))
        return keypairs

    def setUp(self) -> None:
        self.url = get_env('LOCAL_URL')
        self.w3 = w3_conn(self.url)
