#! /usr/bin/env python
# -*- coding: utf8 -*-

"""DSA implementation. Used to prove that ECDSA is better.
"""

__version__ = "$Revision$"
# $Id$

import os
from time import clock

# checks if we are running from a s60 phone and modifies include path
if os.name == 'e32':
    from pys60crypto import sha256
else:
    from hashlib import sha256

import ec
import dsa_keys  # after everything is done, this guy will be removed
import hash_drbg
from modular import mod_inverse, power

random = None

def _sign(m, p, q, g, x, k):
    r = power(g, k, p) % q
    s = (mod_inverse(k, q) * (m + x * r)) % q
    return (r, s)

def _verify(m, r, s, p, q, g, y):
    w = mod_inverse(s, q)
    u1 = m*w % q
    u2 = r*w % q

    v = power(g, u1, p)
    v = (v * power(y, u2, p)) % p
    v = v % q

    return v == r

def sign(message, p, q, g, x, timing_list = None):
    global random

    if random == None:
        random = hash_drbg.HashDRBG()

    k = random(500)

    if timing_list is None:
        message = long(sha256(message).hexdigest(), 16)
        return _sign(message, p, q, g, x, k)

    begin_time = clock()
    r, s = _sign(message, p, q, g, x, k)
    timing_list.append(clock() - begin_time)

    return (r, s)

def verify(message, r, s, p, q, g, y, timing_list = None):

    if timing_list is None:
        message = long(sha256(message).hexdigest(), 16)
        return _verify(message, r, s, p, q, g, y)

    begin_time = clock()
    result = _verify(message, r, s, p, q, g, y)
    timing_list.append(clock() - begin_time)

    return result


def run_tests():
    key_sizes = (1024, 2048, 3072)
    message = "Alice, send me 100 bucks. --Bob"
    message = long(sha256(message).hexdigest(), 16)

    for i in key_sizes:
        pubkey  = getattr(dsa_keys, "pub_%d"  % (i,))
        privkey = getattr(dsa_keys, "priv_%d" % (i,))
        p = getattr(dsa_keys, "p_%d" % (i,))
        q = getattr(dsa_keys, "q_%d" % (i,))
        g = getattr(dsa_keys, "g_%d" % (i,))

        time_sign = []
        time_verify = []

        for n in xrange(15):
            r, s = sign(message, p, q, g, privkey, time_sign)
            verify(message, r, s, p, q, g, pubkey, time_verify)

        fp = file("e:\\ecc4pys60\\sign_%d.txt" % (i,))
        for x in time_sign:
            fp.write("%f\r\n" % (x,))
        fp.close()

        fp = file("e:\\ecc4pys60\\verify_%d.txt" % (i,))
        for x in time_verify:
            fp.write("%f\r\n" % (x,))
        fp.close()
