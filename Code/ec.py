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
    
    if not curve.pointIsInCurve(self):
      print "Point is not valid!"
  
 # SPECIAL METHODS #############################################################################################
  def __repr__(self):
    """
    Returns a string representation of the point.
    
    @rtype: C{str}
    """
    if self.__zero:
      return "(0, 0, True)"
    return "(%d, %d, False)" % (self.__x, self.__y)
    
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
      raise ValueError("4a^3 + 27b^2 == 0 (mod %X)" % (self.__mod,))
    
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
    return "y**2 == x**3 + %X * x + %X (mod %X)" % (self.__a, self.__b, self.__mod)
    
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