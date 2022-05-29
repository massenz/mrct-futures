#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.
import json
import os
import pathlib
import re

from sh import npx


ADDRESSES = 'addresses.json'
ENV = '.env'
KEYVALUE_PATTERN = r"\s*(?P<key>[^#]\w+)\s*=\s*[\"']?(?P<value>[^\"']+)[\"']?"


def get_env(key):
    """ Retrieves an env var from the ENV location

     It will optionally prefix it with `0x` if the property is deemed to be `hex` (the default)
     and it does not have it already.
    """
    if not pathlib.Path(ENV).exists():
        raise RuntimeError(f"File {ENV} does not exit")

    with open(ENV, 'r') as env:
        for line in env.readlines():
            m = re.match(KEYVALUE_PATTERN, line)
            if m and m['key'] == key:
                return m['value']
    raise KeyError(f"{key} not found in {ENV}")


def get_addresses(filedir=None):
    filedir = filedir or os.getcwd()
    with open(os.sep.join([filedir, ADDRESSES])) as addresses:
        return json.load(addresses)
