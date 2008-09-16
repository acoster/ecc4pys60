#! /usr/bin/env python
# -*- coding: utf8 -*-
  
import math
import random

# checks if we are running from a s60 phone and modifies include path
import os
import sys

if os.name == 'e32':
  sys.path.append('e:\ecc4pys60')

# $Id$
__version__   = "$Revision$"
__author__    = "Alexandre Coster"
__contact__   = "acoster at inf dot ufrgs dot br"
__copyright__ = "Copyright (C) 2008 by  Alexandre Coster"

def random_bytes(nBits):
  if sys.version[:2] > (2, 2):
    return random.randint(nLength, 2**nBits - 1)
  
  # The random number is generated in chunks of 16 bits
  nBits /= 16
  nResult = 0
  for nI in xrange(nBits):
    nResult |= random.randint(0, 2**16 - 1) << (16 * nI)
  return nResult

def mod_inverse(nValue, nModulus):
  """Inverse of a mod m."""

  if nValue < 0 or nModulus <= nValue:
    nValue %= nModulus

  nC,  nD = nValue, nModulus
  nUC, nVC, nUD, nVD = 1, 0, 0, 1
  
  while nC != 0:
    nQ, nC, nD = divmod(nD, nC) + (nC,)
    nUC, nVC, nUD, nVD = nUD - nQ * nUC, nVD - nQ * nVC, nUC, nVC

  # asserts the number has a modular inverse
  assert nD == 1
  
  if nUD > 0:
    return nUD
  return nUD + nModulus