#! /usr/bin/env python
# -*- coding: utf8 -*-

__version__ = "$Revision$"
# $Id$

import math
import random

# checks if we are running from a s60 phone and modifies include path
import os
import sys

if os.name == 'e32':
  sys.path.append('e:\ecc4pys60')



def mod_inverse(a, modulus):
    """
    Inverse of a mod m.

    """

    if a < 0 or modulus <= a:
        a %= modulus

    c, d = a, modulus
    uc, vc, ud, vd = 1, 0, 0, 1

    while c != 0:
        q, c, d = divmod(d, c) + (c,)
        uc, vc, ud, vd = ud - q * uc, vd - q * vc, uc, vc

    # asserts the number has a modular inverse
    assert d == 1

    if ud > 0:
        return ud
    return ud + modulus

def power(a, m, n):
    """
    Fast implementation of a**m % n

    """

    assert m >= 0
    assert n >= 1

    ans = 1
    apow = a

    while m != 0:
        if m%2 != 0:
            ans = (ans * apow) % n
        apow = (apow * apow) % n
        m /= 2
    return ans % n
