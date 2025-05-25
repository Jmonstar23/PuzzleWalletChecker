#!/usr/bin/env python3
"""
By Jmon ft Copilot
Module/Function for generating a wallet address to check from the 24word Mnemonic
seed phrases generated in the Mnemonic_generator module. 
"""
# wallet_gen.py
import logging
try:
    import bip32utils
except ImportError:
    raise ImportError("Please install bip32utils (pip install bip32utils)")
try:
    from mnemonic import Mnemonic
except ImportError:
    raise ImportError("Please install mnemonic (pip install mnemonic)")

def generate_wallet_address(mnemonic):
    """
    Given a mnemonic list, generate the bitcoin wallet address.
    """
    mnemonic_str = " ".join(mnemonic)
    logging.debug(f".•.:Generating·.wallet·°from˙°mnemonic°˚·.:[{mnemonic_str}].o•º˚°˚")
    try:
        mobj = Mnemonic("english")
        seed = mobj.to_seed(mnemonic_str)
        wallet_key = bip32utils.BIP32Key.fromEntropy(seed)
        wallet_addr = wallet_key.Address()
        logging.debug(f"˚°˚º•o.»>Derived(~/[wallet]\~)address: {wallet_addr}")
        return wallet_addr
    except Exception as e:
        logging.error(f"˚°˚º•o.![ERROR] wallet generation failed: {e}")
        return None
