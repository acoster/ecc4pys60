import modular

class CEllipticCurvePrime (object): 
  def __init__(self, a, b, mod):
    self.__a    = a
    self.__b    = b
    self.__mod  = mod
    
    # condition for cuvers over a prime field
    if 4*(a ** 3) + 27*(b ** 2) == 0:
      raise ValueError("4a^3 + 27b^2 == 0")
    

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