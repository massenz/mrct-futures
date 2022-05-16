# Copyright AlertAvert.com (c) 2017. All rights reserved.
# Created by Marco Massenzio (marco@alertavert.com), 2017-09-03

import os
import tempfile
import unittest

from utils import run_hh_script


class TestBase(unittest.TestCase):

    contract_addr = None

    def setUpClass() -> None:
        tests_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(os.sep.join([tests_dir, '..']))
        print(f"Deploying contract from {os.getcwd()}")
        TestBase.contract_addr = run_hh_script('deploy.js').strip()
        print(f"Contract address: {TestBase.contract_addr}")

    @staticmethod
    def temp_filename(suffix=None):
        """ Returns a temporary file."""
        filename = tempfile.mkstemp(suffix=suffix)[1]
        return filename
