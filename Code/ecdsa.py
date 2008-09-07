#! /usr/bin/env python
# -*- coding: utf8 -*-

import copy
import math
import random
import md5

# checks if we are running from a s60 phone and modifies include path
import os
import sys
import time

if os.name == 'e32':
  sys.path.append('e:\ecc4pys60')

import ec
from modular import mod_inverse
  
# $Id: ec.py 13 2008-09-07 03:15:18Z acoster $
__version__   = "$Revision: 13 $"
__author__    = "Alexandre Coster"
__contact__   = "acoster at inf dot ufrgs dot br"
__copyright__ = "Copyright (C) 2008 by  Alexandre Coster"

def Sign(nE, oG, nD, nK):
  if oG.nOrder == None:
    raise RuntimeError, "Base point must have order."
    
  nOrder = oG.nOrder
  nK     = nK % nOrder
  oP     = nK * oG
  nR     = oP.nX
  
  if nR == 0:
    raise RuntimeError, "Invalid random number provided (r == 0)"
  
  nS = (mod_inverse(nK, nOrder) * (nE + (nD * nR) % nOrder)) % nOrder
  
  if nS == 0:
    raise RuntimeError, "Invalid random number provided (s == 0)"
  
  return (nR, nS)


def Verify(nR, nS, nE, oG, oQ):
  if oG.nOrder == None:
    raise RuntimeError, "Base point must have order."
    
  nOrder = oG.nOrder
  if nR < 1 or nR > nOrder - 1:
    return False
  if nS < 1 or nS > nOrder - 1:
    return False
    
  nW  = mod_inverse(nS, nOrder)
  nU1 = (nE * nW) % nOrder
  nU2 = (nR * nW) % nOrder
  oP  = nU1 * oG + nU2 * oQ
  
  nV  = oP.nX % nOrder
  return nV == nR
  
p = 6277101735386680763835789423207666416083908700390324961279L
r = 6277101735386680763835789423176059013767194773182842284081L
s = 0x3045ae6fc8422f64ed579528d38120eae12196d5L
c = 0x3099d2bbbfcb2538542dcd5fb078b6ef5f3d6fe2c745de65L
b = 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1L
Gx = 0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012L
Gy = 0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811L

c192 = ec.CEllipticCurvePrime(-3, b, p)
p192 = ec.CECPoint(c192, Gx, Gy, r)
  
nR, nS = Sign(6666, p192, 34, 23423)
print Verify(nR, nS, 6666, p192, 34 * p192)