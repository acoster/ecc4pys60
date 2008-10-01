#! /usr/bin/env python
# -*- coding: utf8 -*-

__version__ = "$Revision$"
# $Id$

import ec

__all__ = ['curve_p192', 'point_p192', 'curve_p224', 'point_p224']

# P-192 curve
curve_p192 = ec.EllipticCurvePrime(-3,
        0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1,
        0xfffffffffffffffffffffffffffffffeffffffffffffffff)
point_p192 = ec.ECPoint(curve_p192,
        0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012,
        0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811,
        0xffffffffffffffffffffffff99def836146bc9b1b4d22831)

# P-224 curve
curve_p224 = ec.EllipticCurvePrime(-3,
        0xb4050a850c04b3abf54132565044b0b7d7bfd8ba270b39432355ffb4,
        0xffffffffffffffffffffffffffffffff000000000000000000000001)
point_p224 = ec.ECPoint(curve_p224,
        0xb70e0cbd6bb4bf7f321390b94a03c1d356c21122343280d6115c1d21,
        0xbd376388b5f723fb4c22dfe6cd4375a05a07476444d5819985007e34)
