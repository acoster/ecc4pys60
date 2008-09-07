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

from modular import mod_inverse
  
# $Id$
__version__   = "$Revision$"
__author__    = "Alexandre Coster"
__contact__   = "acoster at inf dot ufrgs dot br"
__copyright__ = "Copyright (C) 2008 by  Alexandre Coster"

def LeftmostBit(nX):
  assert nX > 0
  
  nResult = 1L
  while nResult <= nX:
    nResult = 2 * nResult
  return nResult / 2

class CEllipticCurvePrime(object): 
  """
  Abstraction of an Elliptic Curve over a prime field. It is defined as M{y**2 = x**3  + ax + b (mod p)}.
  """
  
  def __init__(self, nA, nB, nModulus):
    self.__nA       = nA
    self.__nB       = nB
    self.__nModulus = nModulus
  
  def IsOnCurve(self, oPoint):
    return (oPoint.nY**2 - (oPoint.nX**3 + self.__nA * oPoint.nX + self.__nB)) % self.__nModulus == 0
    
  def nA(self):
    return self.__nA
  nA = property(nA)
    
  def nB(self):
    return self.__nB
  nB = property(nB)
  
  def nModulus(self):
    return self.__nModulus
  nModulus = property(nModulus)
  
class CECPoint(object):
  def __init__(self, oCurve = None, nX = None, nY = None, nOrder = None):
    self.__oCurve = oCurve
    self.__nX     = nX
    self.__nY     = nY
    self.__nOrder = nOrder
    
    if oCurve and nX and nY:
      assert oCurve.IsOnCurve(self)
    
    if nOrder:
      assert self * nOrder == g_oInfinity
      
# UNARY OPERATORS ##############################################################################################
  def __neg__(self):
    return CECPoint(self.__oCurve, self.__nX, -self.__nY, self.__nOrder)

# BINARY OPERATORS #############################################################################################      
  def __eq__(self, oRight):
    return self.__oCurve == oRight.__oCurve and \
           self.__nX     == oRight.__nX     and \
           self.__nY     == oRight.__nY
  
  def __add__(self, oRight):
    if oRight == g_oInfinity:
      return self
    
    if self == g_oInfinity:
      return oRight
    
    assert self.__oCurve == oRight.__oCurve
    
    if self.__nX == oRight.__nX:
      if (self.__nY + oRight.__nY) % self.__oCurve.nModulus == 0:
        return g_oInfinity
      return self.Double()
    
    nModulus = self.__oCurve.nModulus
    nLambda  = ((oRight.__nY - self.__nY) * mod_inverse(oRight.__nX - self.__nX, nModulus)) % nModulus
    
    nX3 = (nLambda**2 - self.__nX - oRight.__nX)    % nModulus
    nY3 = (nLambda * (self.__nX - nX3) - self.__nY) % nModulus
    
    return CECPoint(self.__oCurve, nX3, nY3)
  
  def __mul__(self, nRight): 
    if self.__nOrder:
      nRight = nRight % self.__nOrder
    
    if nRight == 0 or self == g_oInfinity:
      return g_oInfinity
    
    assert nRight > 0

    nRight3  = 3 * nRight
    oNegSelf = -self
    nI       = LeftmostBit(nRight3) / 2
    oResult  = self
    
    while nI > 1:
      oResult = oResult.Double()
      if (nRight3 & nI) != 0 and (nRight & nI) == 0:
        oResult = oResult + self
      if (nRight3 & nI) == 0 and (nRight & nI) != 0:
        oResult = oResult + oNegSelf
      nI = nI / 2
    
    return oResult
  
# REVERSE BINARY OPERATORS #####################################################################################
  def __rmul__(self, nLeft):
    return self * nLeft


# OTHER METHODS ################################################################################################    
  def Double(self):
    nModulus = self.__oCurve.nModulus
    nA       = self.__oCurve.nA

    nLambda = ((3 * self.__nX**2 + nA) * mod_inverse(2 * self.__nY, nModulus)) % nModulus
    nX      = (nLambda**2 - 2 * self.__nX)                                     % nModulus
    nY      = (nLambda * (self.__nX - nX) - self.__nY)                         % nModulus
    
    return CECPoint(self.__oCurve, nX, nY)
    
# PROPERTIES ###################################################################################################
  def nX(self):
    return self.__nX
  nX = property(nX)
  
  def nY(self):
    return self.__nY
  nY = property(nY)
  
  def oCurve(self):
    return self.__oCurve
  oCurve = property(oCurve)
  
  def nOrder(self):
    return self.__nOrder
  nOrder = property(nOrder)

# Infinity point
g_oInfinity = CECPoint()