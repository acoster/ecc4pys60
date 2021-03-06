#! /usr/bin/env python
# -*- coding: utf8 -*-

__version__ = "$Revision$"
# $Id$

import os
from time import clock
from math import log, ceil

# checks if we are running from a s60 phone and modifies include path
if os.name == 'e32':
    from pys60crypto import sha256
else:
    from hashlib import sha256

import ec
import hash_drbg
import nist_curves
from modular import mod_inverse

__all__ = ['generate_key_pair', 'sign', 'verify']

random = None

class InvalidRandomNumber(Exception):
    pass

### INTERNAL FUNCTIONS ########################################################
def _sign(e, G, d, k):
    if G.order == None:
        raise RuntimeError("Base point must have order.")

    order = G.order
    k = k % order
    p = G * k
    r = p.x

    if r == 0:
        raise InvalidRandomNumber("Invalid random number provided (r == 0)")

    s = (mod_inverse(k, order) * (e + (d * r) % order)) % order

    if s == 0:
        raise InvalidRandomNumber("Invalid random number provided (s == 0)")

    return (r, s)

def _verify(r, s, e, G, Q):
    if G.order == None:
        raise RuntimeError("Base point must have order.")

    order = G.order
    if r < 1 or r > order - 1:
        return False
    if s < 1 or s > order - 1:
        return False

    w = mod_inverse(s, order)
    u1 = (e * w) % order
    u2 = (r * w) % order

    p = G.MultiplyPoints(u1, Q, u2)

    v = p.x % order
    return v == r


### PUBLIC FUNCTIONS ##########################################################
def generate_key_pair(G):
    """
    Returns a tuple containing the private key (a long integer) and the
    public key (the point G multiplied by the private key).

    """

    global random

    if random == None:
        random = hash_drbg.HashDRBG()

    if G.order == None:
        raise RuntimeError("Base point must have order.")

    key_size = log(ec.leftmost_bit(G.order)) / log(2)
    key_size = int(ceil(key_size) / 2)
    private_key = 1

    while private_key <= 1:
        private_key = random(key_size) #generates a random number
                                       #with twice the required bits
        private_key %= G.order

    return (private_key, G * private_key)


def sign(message, G, d, timing_list = None):
    """
    Signs the string `message` using the private key `d` and the
    point `G`.

    """

    global random

    if random is None:
        random = hash_drbg.HashDRBG()

    k = random(128)

    if timing_list == None:
        return _sign(long(sha256(message).hexdigest(), 16), G, d, k)

    begin_time = clock()
    signature = _sign(message, G, d, k)
    timing_list.append(clock() - begin_time)

    return signature


def verify(r, s, message, G, Q, timing_list = None):
    """Verifies if the message signature (r, s) is valid to the public
    public key Q.

    """

    if timing_list == None:
        return _verify(r, s, long(sha256(message).hexdigest(), 16), G, Q)

    begin_time = clock()
    result = _verify(r, s, message, G, Q)
    timing_list.append(clock() - begin_time)

    return result


### STATS STUFF ###############################################################
def run_stats():
    """
    Collects stats to signature and signature verification.

    """

    time_signature    = {}
    time_verification = {}

    # this should speed up things
    message = "Alice, send me 100 bucks. --Bob"
    message = long(sha256(message).hexdigest(), 16)

    curvas = [(i, getattr(nist_curves, i)) for i in dir(nist_curves) if
                                                    i.startswith("point_p")]

    for name, point in curvas:
        priv_key, pub_key = generate_key_pair(point)
        time_signature[name] = []
        time_verification[name] = []

        for i in xrange(30):
            r, s = sign(message, point, priv_key, time_signature[name])
            status = verify(r, s, message, point, pub_key,
                                                    time_verification[name])

        print "%s done" % (name, )

    return (time_signature, time_verification)

results = run_stats()
