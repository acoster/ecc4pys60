import math

# VCS information
__revision__ = "$Revision$"
__id__       = "$Id$"
__date__     = "$Date$"
__headurl__  = "$HeadURL$"

class CModInt(object):
  __unsupported_types = (float, str)

  def __init__(self, n, mod):
    self.__mod = mod
    
    if n < 0:
      self.__n = (mod + n) % mod
    else:
      self.__n = n % mod
  
  def __repr__(self):
    return "%d (mod %d)" % (self.__n, self.__mod)
  
# PROPERTIES ###################################################################################################
  def n(self):
    return self.__n
  n = property(n)
  
  def mod(self):
    return self.__mod
  mod = property(mod)

# COMPARSION OPERATORS #########################################################################################      
  def __eq__(self, right):
    if isinstance(right, CModInt):
      return self.__mod == right.mod and self.__n == right.n
    return self.__n == right
    
# "CAST" OPERATORS #############################################################################################
  def __int__(self):
    return int(self.__n)
  
  def __long__(self):
    return long(self.__n)
    
# UNARY OPERATORS ##############################################################################################
  def __neg__(self):
    return CModInt(-self.__n, self.__mod)  
  
# ARITHIMETIC OPERATORS ######################################################################################## 
  def __add__(self, right):
    if isinstance(right, CModInt):
      if self.__mod != right.mod:
        raise ValueError("Integers are not congruent to same modulo!")
      return CModInt(self.__n + right.n, self.__mod)
    
    if right.__class__ in self.__unsupported_types:
      raise TypeError("unsupported operand types for +: CModInt and %s" % (right.__class__, ))
      
    return CModInt(self.__n + right, self.__mod)
    
  def __sub__(self, right):
    if isinstance(right, CModInt):
      if self.__mod != right.mod:
        raise ValueError("Integers are not congruent to same modulo!")
      return CModInt(self.__mod + self.__n - right.n, self.__mod)
    
    if right.__class__ in self.__unsupported_types:
      raise TypeError("unsupported operand types for -: CModInt and %s" % (right.__class__, ))
      
    return CModInt(self.__mod + self.__n - right, self.__mod)
  
  def __mul__(self, right):
    if isinstance(right, CModInt):
      if self.__mod != right.mod:
        raise ValueError("Integers are not congruent to same modulo!")
      return CModInt(self.__n * right.n, self.__mod)
    
    if right.__class__ in self.__unsupported_types:
      raise TypeError("unsupported operand types for -: CModInt and %s" % (right.__class__, ))
    
    return CModInt(self.__n * right, self.__mod)
  
  def __pow__(self, right):
    if isinstance(right, CModInt):
      if self.__mod != right.mod:
        raise ValueError("Integers are not congruent to same modulo!")
      return self.__pow__(right.n)
      
    if right == 0.5:
      return CModInt(sqrt(self.__n, self.__mod), self.__mod)
      
    if right.__class__ in self.__unsupported_types:
      raise TypeError("unsupported operand types for -: CModInt and %s" % (right.__class__, ))
    
    if right < 0:
      return CModInt(power(inverse(self.__n, self.__mod), -right, self.__mod), self.__mod)
      
    return CModInt(power(self.__n, right, self.__mod), self.__mod)
    
  def __div__(self, right):
    if isinstance(right, CModInt):
      if self.__mod != right.mod:
        raise ValueError("Integers are not congruent to same modulo!")
      return self * right**-1
    
    return self / CModInt(right, self.__mod)
  
  def __truediv__(self, right):
    return self.__div__(right)

# REVERSE OPERATORS ############################################################################################
  def __radd__(self, left):
    return self + left
    
  def __rsub__(self, left):
    return -self + left
    
  def __rmul__(self, left):
    return self * left
  
  def __rdiv__(self, left):
    return CModInt(left, self.__mod) / self
    
  def __rtruediv__(self, left):
    return __rdiv(self, left)
  
# IN-PLACE OPERATIONS ##########################################################################################
# Defined for performance reasons
  def __iadd__(self, right):
    if isinstance(right, CModInt):
      if self.__mod != right.mod:
        raise ValueError("Integers are not congruent to same modulo!")
      self.__n = (right.n + self.__n) % self.__mod
    
    if right.__class__ in self.__unsupported_types:
      raise TypeError("unsupported operand types for -: CModInt and %s" % (right.__class__, ))  
    
    self.__n = (right + self.__n) % self.__mod
    
  
  def __isub__(self, right):
    if isinstance(right, CModInt):
      if self.__mod != right.mod:
        raise ValueError("Integers are not congruent to same modulo!")
      self.__n = (self.__mod + self.__n - right.n) % self.__mod
    
    if right.__class__ in self.__unsupported_types:
      raise TypeError("unsupported operand types for -: CModInt and %s" % (right.__class__, ))
    
    self.__n = (self.__mod + self.__n - right) % self.__mod
# END OF CLASS #################################################################################################

def gcd(a, b):
  x = [0, 1]
  y = [1, 0]

  if a*b == 0:
    raise ZeroDivisionError()

  if a > b:
    result = gcd(b, a)
    return (result[0], result[2], result[1])

  j = 1

  while b != 0:
    if j > 1:
      x.append(-q * x[j - 1] + x[j - 2])
      y.append(-q * y[j - 1] + y[j - 2])

    q  = a/b
    j += 1
    t  = b
    b  = a%b
    a  = t

  return (a, x[-1], y[-1])

def inverse(a, n):
  result = gcd(a, n)
  return result[2]

def power(x, y, n):
  if y == 0:
    if x != 0:
      return 1
    else:
      raise ZeroDivisionError()
      
  if y == 1:
    return x % n

  powers = [x]

  l = int(math.ceil(math.log(y) / 0.69314718055994529)) + 1

  for i in xrange(l - 1):
    powers.append(powers[-1] ** 2 % n)

  return reduce(lambda x, y:(x * y) % n, [powers[z] for z in range(l) if (y & 2**z) != 0], 1)

def sqrt(x, p):
  if p % 4 == 3:
    return power(x, (p + 1) / 4, p)
  else:
    num = range(p)
    num.reverse()
    
    for i in num:
      if i**2 % p == x % p:
        return i