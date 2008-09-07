#! /usr/bin/env python
# -*- coding: utf8 -*-

import copy
import math
import random
import md5

# checks if we are running from a s60 phone and modifies include path
import os
import sys

if os.name == 'e32':
  sys.path.append('e:\ecc4pys60')

import ec
from modular import mod_inverse
  
# $Id$
__version__   = "$Revision$"
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
  
  #oP  = nU1 * oG + nU2 * oQ 
  oP = oG.MultiplyPoints(nU1, oQ, nU2)
  
  nV  = oP.nX % nOrder
  return nV == nR