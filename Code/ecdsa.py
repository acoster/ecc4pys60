#! /usr/bin/env python
# -*- coding: utf8 -*-

__version__ = "$Revision$"
# $Id$

import os
import sys
from math import log, ceil

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

### INTERNAL FUNCTIONS ########################################################
def _sign(e, G, d, k):
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

### PUBLIC FUNCTIONS ##########################################################
def generate_key_pair(G):
    if G.order == None:
        raise RuntimeError("Base point must have order.")

    random_generator = hash_drbg.HashDRBG()

    key_size = log(ec.leftmost_bit(G.order)) / log(2)
    key_size = ceil(key_size) / 2
    private_key = 1

    while private_key <= 1:
        private_key = random_generator(key_size) #generates a random number
                                                 #with twice the required bits
        private_key %= G.order

    return (private_key, G * private_key)

def sign(message, G, d):
    r = hash_drbg.get_entropy(1024)
    return _sign(long(sha256(message).hexdigest, 16), G, d, k)
