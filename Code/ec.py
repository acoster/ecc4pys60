#! /usr/bin/env python
# -*- coding: utf8 -*-

import copy
import math
import random

# checks if we are running from a s60 phone and modifies include path
import os
import sys
import time

if os.name == 'e32':
  sys.path.append('e:\ecc4pys60')

import modular

# $Id$
__version__   = "$Revision$"
__author__    = "Alexandre Coster"
__contact__   = "acoster at inf dot ufrgs dot br"
__copyright__ = "Copyright (C) 2008 by  Alexandre Coster"

class CECDH(object):
  """
  
  """

  def __init__(self, oCurve, nBaseX, nBaseY, nMultiplicator):
    """
    """
    
    self.__oCurve         = oCurve
    self.__oBasePoint     = CECPoint(nBaseX, nBaseY, oCurve)
    self.__nMultiplicator = nMultiplicator
    self.__oPubPoint      = self.__oBasePoint * nMultiplicator
    
  def GenKey(self, oPoint):
    return oPoint * self.__nMultiplicator
    
  def MyPoint(self):
    return copy.copy(self.__oPubPoint)
  MyPoint = property(MyPoint)

class CECPoint(object):
  """
  Representation of a point (x, y) over an elliptic curve modulo G.
  """
 
  def __init__(self, x, y, curve, zero = False):
    """
    Constructor for a point object.
    
    @param x: x coordinate of the point.
    @param y: y coordinate of the point.
    @param curve: cuve over which the point is defined.
    @param zero: defined C{True} if this is "0".
    
    @type x: C{long}, C{int} or L{CModInt}
    @type y: C{long}, C{int} or L{CModInt}
    @type curve: L{CEllipticCurvePrime}
    @type zero: C{int} or C{bool}
    @rtype: L{CECPoint}
    """
  	
    if not isinstance(x, modular.CModInt):
      self.__x = modular.CModInt(x, curve.mod)
    else:
      self.__x = x
    
    if not isinstance(y, modular.CModInt):
      self.__y = modular.CModInt(y, curve.mod)
    else:
      self.__y = y
    
    self.__curve = curve
    self.__zero  = zero
    
    #if not curve.pointIsInCurve(self):
    #  print "Point is not valid!"
  
 # SPECIAL METHODS #############################################################################################
  def __repr__(self):
    """
    Returns a string representation of the point.
    
    @rtype: C{str}
    """
    if self.__zero:
      return "(0, 0, True)"
    return "(%x, %x, False)" % (long(self.__x), long(self.__y))
    
# UNARY OPERATORS ##############################################################################################
  def __neg__(self):
    """
    Returns the additive inverse of a point.
    
    @rtype: L{CECPoint}
    """
    return CECPoint(self.__x, -self.__y, self.__curve, self.__zero)
	
# BINARY OPERATORS #############################################################################################
  def __eq__(self, right):
    if not isinstance(right, CECPoint):
      return False
      
    if self.__curve != right.curve:
      return False
      
    return (self.__x == right.x and self.__y == right.y) or self.__zero == right.zero
    
  def __add__(self, right):
    """
    Returns the resulting point of C{self} + C{right}.
    
    @param right: right-side of operation
    @type right: L{CECPoint}
    @rtype: L{CECPoint}
    """
    if not isinstance(right, CECPoint):
      raise ValueError("Right of operation must be of type CECPoint!")
    
    if self.__curve != right.curve:
      raise ValueError("Points must be defined over the same curve!")
    
    # "Declaring" the var.
    m = None
    
    if self.__zero:
      return CECPoint(right.x, right.y, self.__curve, right.zero)
    
    if right.zero:
      return CECPoint(self.__x, self.__y, self.__curve, self.__zero)
    
    if self.__x != right.x:
      m = (self.__y - right.y)/(self.__x - right.x)
    elif self.__y != right.y or right.y == 0:
      return CECPoint(0, 0, self.__curve, True)
    else:
      m = (3 * right.x**2 + self.__curve.a)/(2 * right.y)
    
    x = m**2 - self.__x - right.x
    y = m * (right.x - x) - right.y
    
    return CECPoint(x, y, self.__curve)
    
  def __sub__(self, right):
    return self + -right
    
  def __mul__(self, right):   
    """
    Returns the resulting point of C{self} * C{right}.
    
    @param right: right-side of operation
    @type right: C{int} or C{long}
    @rtype: L{CECPoint}
    """
    if isinstance(right, modular.CModInt):
      if right.mod != self.__curve.mod:
        raise ValueError("Point has different modulo than curve!")
        
      right = right.n
    
    if isinstance(right, float):
      return NotImplemented
    
    if right == 0:
      return CECPoint(0, 0, self.__curve, True)
    
    # threat "pathologic" cases
    if right == 1:
      return copy.copy(self)
    
    result = None
    p = copy.copy(self)
    n = 1L
    strRes = ''
    
    
    while n <= right:
      if n & right != 0:
        if result == None:
          result = copy.copy(p)
        else:
          result = result + p
      p = p + p
      n = n<<1
    
    return result
  
# INVERSE OPERATORS ############################################################################################
  def __rmul__(self, left):
    return self * left
 
# ACCESSOR METHODS #############################################################################################
  def x(self):
    return self.__x
  x = property(x)
  """
  Point's x coordinate
  @type: L{CModInt}
  """
  
  def y(self):
    return self.__y
  y = property(y)
  """
  Point's y coordinate
  @type: L{CModInt}
  """
  
  def zero(self):
    return self.__zero
  zero = property(zero)
  """
  True if the point is "zero", false otherwise.
  @type: C{bool}
  """
  
  def curve(self):
    return self.__curve
  curve = property(curve)
  """
  Cuver over which the point is defined.
  @type: L{CEllipticCurvePrime}
  """


class CEllipticCurvePrime(object): 
  """
  Abstraction of an Elliptic Curve over a prime field. It is defined as M{y**2 = x**3  + ax + b (mod p)}.
  """
  
  def __init__(self, a, b, mod):
    """
    Instantiates an elliptic curve over a prime field.
    
    @param a: The M{a} constant.
    """
    if not isinstance(a, modular.CModInt):
      self.__a = modular.CModInt(a, mod)
    else:
      self.__a = a
    
    if not isinstance(b, modular.CModInt):
      self.__b = modular.CModInt(b, mod)
    else:
      self.__b = b
    self.__mod  = mod
    
    # checks if the curve is valid
    if 4 * self.__a ** 3 + 27 * b ** 2 == 0:
      raise ValueError("4a^3 + 27b^2 == 0 (mod %lx)" % (self.__mod,))
    
  def pointIsInCurve(self, point):
    """
    Checks if the given point sits in the curve.
    
    @param point: Point that we want to check.
    @type point: L{CECPoint}
    @rtype: C{bool}
    """
    
    if not isinstance(point, CECPoint):
      raise TypeError("point should be of type CECPoint, not %s" % (point.__class__,))
    
    return point.zero or point.y**2 == (point.x**3 + self.__a * point.x + self.__b)

# SPECIAL METHODS ##############################################################################################    
  def __repr__(self):
    """
    String representation function.
    
    @rtype: C{str }
    """
    return "y**2 == x**3 + %lx * x + %lx (mod %x)" % (long(self.__a), long(self.__b), long(self.__mod))
    
  def __eq__(self, right):
    if not isinstance(right, CEllipticCurvePrime):
      return False
  
    return self.a == right.a and self.b == right.b and self.mod == right.mod
    
  # generates a point
  def __call__(self, x):
    """
    Returns a tuple with all points at the given M{x}. It might be empty if there is no defined point at point.
    
    @param x: The x-coordinate of the point.
    @type  x: C{int}, C{long} or L{CModInt}
    @rtype: tuple
    """
    if not isinstance(x, modular.CModInt):
      x = modular.CModInt(x, self.__mod)
    
    # this is the more memory efficient way (as all operations are in-place)
    y   = x**2
    y  += self.__a
    y  *= x
    y  += self.__b   
    y **= 0.5

    # no square root, so no point
    if y == None:
      return ()
    
    # only one point there...
    if y == 0:
      return (CECPoint(x, y, self), )
    
    return (CECPoint(x, y, self), CECPoint(x, -y, self))

# ACESSOR METHODS ##############################################################################################
  def a(self):
    return self.__a
  a = property(a)
  
  def b(self):
    return self.__b
  b = property(b)
  
  def mod(self):
    return self.__mod
  mod = property(mod)
  
def Test():
  nP         = 26959946667150639794667015087019630673557916260026308143510066298881
  nA         = modular.CModInt(-3, nP)
  nB         = modular.CModInt(0xb4050a850c04b3abf54132565044b0b7d7bfd8ba270b39432355ffb4, nP)
  oCurve     = CEllipticCurvePrime(nA, nB, nP)
  
  nGX        = 0xb70e0cbd6bb4bf7f321390b94a03c1d356c21122343280d6115c1d21
  nGY        = 0xbd376388b5f723fb4c22dfe6cd4375a05a07476444d5819985007e34
  
  nAX = 0xc5d85abbd81d212902c16c5c6857be72f36370e1749b78e682a26e21
  nAY = 0x7ffc0818343a5c5bdc869254dfefe132c0e414dbccd28278eee40c1d
  
  oBasePoint  = CECPoint(nGX, nGY, oCurve)
  oAlicePoint = CECPoint(nAX, nAY, oCurve)
  
  cl = time.clock()
  #oDHAlice = CECDH(oCurve, nGX, nGY, long(random.random() * nP-1))
  oDHBob  = CECDH(oCurve, nGX, nGY, long(random.random() * nP-1))
  print oDHBob.GenKey(oAlicePoint)
  print time.clock() - cl
  