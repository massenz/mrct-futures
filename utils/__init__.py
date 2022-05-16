#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.
import os
import pathlib

from sh import npx


ENV = '.env'


def get_env(key, is_hex=True):
    """ Retrieves an env var from the ENV location

     It will optionally prefix it with `0x` if the property is deemed to be `hex` (the default)
     and it does not have it already.
    """
    if not pathlib.Path(ENV).exists():
        raise RuntimeError(f"File {ENV} does not exit")

    with open(ENV, 'r') as env:
        for line in env.readlines():
            if line.startswith('#'):
                continue
            # TODO: Use a RegEx instead
            if line.startswith(key):
                pk = line.split("=")[1].replace('"', '').strip()
                if is_hex and not pk.startswith('0x'):
                    pk = '0x' + pk
                return pk
    raise KeyError(f"{key} not found in {ENV}")


def run_hh_script(script, scripts_dir='scripts', network='local'):
    """Runs the Hardhat `script` in the `scripts_dir`, against the given network."""
    script_path = os.sep.join([scripts_dir, script])
    cmd = npx.hardhat("--network", network, "run", script_path)
    # Here we convert the bytes output to string, remove any trailing newlines and then return
    # only the last line (the contract's deployed address).
    return cmd.stdout.decode().strip().split('\n')[-1]
