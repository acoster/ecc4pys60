import modular
import math

# VCS information
__revision__ = "$Revision"
__id__       = "$Id$"
__date__     = "$Date$"
__headurl__  = "$HeadURL$"

class CECPoint(object): 
  def __init__(self, x, y, curve, infinity = False):
    self.__x        = x
    self.__y        = y
    self.__curve    = curve
    self.__infinity = infinity
  
 # OPERATOR OVERLOAD/SPECIAL METHODS ###########################################################################
  def __repr__(self):
    return "(%d, %d)" % (self.__x, self.__y)
    
  def __add__(self, right):
    if not isinstance(right, CECPoint):
      raise ValueError("Right of operation must be of tzpe CECPoint!")
    
    if self.curve != right.curve:
      raise ValueError("Points must be defined over the same curve!")
    
    m = None
    if self == right:
      if self.y == 0:
        return CECPoint(0, 0, self.curve, True)
      m = (right.y - self.y)/(right.x - self.x)
    else:
      if self.x == right.x:
        return CECPoint(0, 0, self.curve, True)
      m = (3 * self.x**2 + curve.a)/(2*self.y)
      
    
    
    x = m**2 - self.x - right.x
    y = m*(self.x - x) - self.y
    
    return CECPoint(x, y, self.curve)
 
# ACCESSOR METHODS #############################################################################################
  def x(self):
    return self.__x
  x = property(x)
  
  def y(self):
    return self.__y
  y = property(y)
  
  def curve(self):
    return self.__curve
  curve = property(curve)

class CEllipticCurvePrime(object): 
  def __init__(self, a, b, mod):
    self.__a    = modular.CModInt(a, mod)
    self.__b    = modular.CModInt(b, mod)
    self.__mod  = mod
    
    # REVIEW condition for cuves over a prime field
    #if (4 * modular.power(a, 3, mod) + 27 * modular.power(b, 2, mod)) % mod == 0:
    #  raise ValueError("4a^3 + 27b^2 == 0")
  
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