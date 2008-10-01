#! /usr/bin/env python
# -*- coding: utf8 -*-

# $Id$
__version__     = "$Revision$"

import os
import sys
import copy
import math
import random

# checks if we are running from a s60 phone and modifies include path
if os.name == 'e32':
    sys.path.append('e:\ecc4pys60')
    from pys60crypto import sha256
else:
    from hashlib import sha256

import ec
import hash_drbg
from modular import mod_inverse

__all__ = ['generate_key_pair', 'sign']

def generate_key_pair(G):
    if G.order == None:
        raise RuntimeError("Base point must have order.")

    key_size = math.log(ec.leftmost_bit(G.order)) / math.log(2)
    key_size = math.ceil(key_size) / 2
    private_key = 1

    while private_key <= 1:
        private_key = hash_drbg.get_entropy(key_size)
        private_key %= G.order

    return (private_key, G * private_key)

def _sign(e, G, d, k):
    """
        e -> message hash
        G -> base point
        d -> private key
        k -> random integer
    """
    if G.order == None:
        raise RuntimeError("Base point must have order.")

    order = G.order
    k = k % order
    p = k * G
    r = p.nX

    if r == 0:
        raise RuntimeError("Invalid random number provided (r == 0)")

    s = (mod_inverse(k, order) * (e + (d * r) % order)) % order

    if s == 0:
        raise RuntimeError("Invalid random number provided (s == 0)")

    return (r, s)

def sign(message, G, d):
    r = hash_drbg.get_entropy(1024)
    return _sign(long(sha256(message).hexdigest, 16), G, d, k)


def _verify(r, s, e, G, Q):
    if G.order == None:
        raise RuntimeError("Base point must have order.")

    order = G.order
    if r < 1 or r > order - 1:
        return False
    if s < 1 or s > order - 1:
        return False

    nW    = mod_inverse(s, order)
    nU1 = (e * nW) % order
    nU2 = (r * nW) % order

    oP = G.MultiplyPoints(nU1, Q, nU2)

    nV    = oP.nX % order
    return nV == r
