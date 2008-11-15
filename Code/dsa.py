#! /usr/bin/env python
# -*- coding: utf8 -*-

"""DSA implementation. Used to prove that ECDSA is better.
"""

__version__ = "$Revision$"
# $Id$

import os
import sys
from time import clock

# checks if we are running from a s60 phone and modifies include path
if os.name == 'e32':
    sys.path.append('e:\ecc4pys60')
    from pys60crypto import sha256
else:
    from hashlib import sha256

import ec
import hash_drbg
from modular import mod_inverse, power
from math import pow

random = None

# 1024 bit test parameters
priv_1024 = 0x5fa027790340dff488a30fe9968db5f0013df3efL
pub_1024 = 0x12c1ab280f4750d698c9f4c8d07e54396a67fdeac84766d308a188518a973d50ed050de5a13f4fa47d6b1394dd923b0c5102e648a85a7b54ff32712fdd43ef92690da1b293d473c0bf1ba05ff9fad1fc068e7564dd72cd1a874069de87fc0ce98dfe6c8193693cd502bb209c23f7887681b569146fd62d3d80ce5eba6d9fe732L
p_1024 = 0x00e3d80600e51ce8126c15f84c48173b829131b84bc590e95f7226149d47a71e09b62ae7f48b7a927677bcc30db540b6a32e3b0c5057260d204e8f00c22718696d0114b371b439fef9ffa650e0c618d9e9d047a9f47190e6fb6ba7d9ddb86adc5b59b5fdb6d484445f1e1e4ed61459b18c12458002ab4c8262ca1bf73b477855d9L
q_1024 = 0x0087331582d0afeb5a5a043eb1987ef30a4a6fd6e7L
g_1024 = 0x01fbd781fceb17fd17983a06eaf0596b1aff0fd078a2231869d85c92598408e2a6cb66991b8e0e7c7e01557e7aa3f22bb6fb60b1ddb7aba9ee1e1504f83c84276d5bae0443aa49d081fb33bb2804b90391519ac28436bcf75fb1aa11b100fc256373c0465fa33f7a443b2ad85cce267290d1b47a7c241cf88dff213a9e9d2de3L


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

def sign(message, p, q, g, x, timing_list):
    global random

    if random == None:
        random = hash_drbg.HashDRBG()

    k = random(500)
    # move this outside
    message = long(sha256(message).hexdigest(), 16)

    begin_time = clock()
    r, s = _sign(message, p, q, g, x, k)
    timing_list.append(clock() - begin_time)

    return (r, s)

def verify(message, r, s, p, q, g, y, timing_list):
    # move this outside for tests...
    message = long(sha256(message).hexdigest(), 16)

    begin_time = clock()
    result = _verify(message, r, s, p, q, g, y)
    timing_list.append(clock() - begin_time)

    return result
