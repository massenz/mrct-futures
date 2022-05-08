#  Copyright (c) M. Massenzio, 2022.
#  All rights reserved.


def get_env(key, envloc=".env", is_hex=True):
    """ Retrieves an env var from the given `envloc` location

     It will optionally prefix it with `0x` if the property is deemed to be `hex` (the default)
     and it does not have it already.
    """
    with open(envloc) as env:
        for line in env.readlines():
            if line.startswith(key):
                pk = line.split("=")[1].replace('"', '').strip()
                if is_hex and not pk.startswith('0x'):
                    pk = '0x' + pk
                return pk
    raise KeyError(f"{key} not found in {envloc}")
