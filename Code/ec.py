#! /usr/bin/env python
# -*- coding: utf8 -*-

import copy
import modular
import math

# $Id$
__version__   = "$Revision$"
__author__    = "Alexandre Coster"
__contact__   = "acoster at inf dot ufrgs dot br"
__copyright__ = "Copyright (C) 2008 by  Alexandre Coster"

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
  
 # SPECIAL METHODS #############################################################################################
  def __repr__(self):
    """
    Returns a string representation of the point.
    
    @rtype: C{str}
    """
    return "(%d, %d)" % (self.__x, self.__y)
    
# UNARY OPERATORS ##############################################################################################
  def __neg__(self):
    """
    Returns the additive inverse of a point.
    
    @rtype: L{CECPoint}
    """
    return CECPoint(self.__x, -self.__y, self.__curve, self.__zero)

# BINARY OPERATORS #############################################################################################    
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
    
    m = None
    
    if self.__zero:
      return CECPoint(right.x, right.y, self.__curve, right.zero)
    
    if right.zero:
      return CECPoint(self.__x, self.__y, self.__curve, self.__zero)
    
    if self == right:
      if self.y == 0:
        return CECPoint(0, 0, self.curve, True)
      m = (3 * self.__x**2 + self.__curve.a)/(2*self.__y)
    else:
      if self.x == right.x:
        return CECPoint(0, 0, self.__curve, True)
      m = (right.y - self.__y)/(right.x - self.__x)
    
    x = m**2 - self.__x - right.x
    y = m*(self.__x - x) - self.__y
    
    return CECPoint(x, y, self.__curve)
    
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
    
    if right == 1:
      return copy.copy(self)
    
    if right%2 == 1:
      return (self + self) * (right/2) + self
    return (self + self) * (right/2)
 
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
  def __init__(self, a, b, mod):
    self.__a    = modular.CModInt(a, mod)
    self.__b    = modular.CModInt(b, mod)
    self.__mod  = mod
    
    # REVIEW condition for cuves over a prime field
    #if (4 * modular.power(a, 3, mod) + 27 * modular.power(b, 2, mod)) % mod == 0:
    #  raise ValueError("4a^3 + 27b^2 == 0")
    
  def pointIsInCurve(self, point):
    """
    Checks if the given point sits in the curve.
    
    @param point: Point that we want to check.
    @type point: L{CECPoint}
    @rtype: C{bool}
    """
    
    if not isinstance(point, CECPoint):
      raise TypeError("point should be of type CECPoint, not %s" % (point.__class__,))
    
    return point.y**2 == (point.x**3 + self.__a * point.x + self.__b)
  
  def __repr__(self):
    return "y**2 == x**3 + %d * x + %d (mod %d)" % (self.__a, self.__b, self.__mod)
    
  def __eq__(self, right):
    if not isinstance(right, CEllipticCurvePrime):
      return False
  
    return self.a == right.a and self.b == right.b and self.mod == right.mod
    
  # generates a point
  def __call__(self, x):
    if not isinstance(x, modular.CModInt):
      x = modular.CModInt(x, self.__mod)
    
    y = x**3 + self.__a * x + self.__b
    y = y**0.5
    
    return CECPoint(x, y, self)

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