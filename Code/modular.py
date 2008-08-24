import math

__date__     = "$Date$"
__headurl__  = "$HeadURL$"
__id__       = "$Id$"
__revision__ = "$Revision$"

def gcd(a, b):
  """
    a is always less or equal than b!
  """

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

    q = a/b
    j += 1
    t = b
    b = a % b
    a = t

  return (a, x[-1], y[-1])

def power(x, y, n):
  if y == 0:
    if x != 0:
      return 1
    else:
      raise ZeroDivisionError()

  powers = [x]

  l = int(math.ceil(math.log(y) / 0.69314718055994529)) + 1

  for i in xrange(l - 1):
    powers.append(powers[-1] ** 2 % n)

  val = {True: 1, False: 0}

  return reduce(lambda x, y:(x * y) % n, [powers[z] for z in range(l)[::-1] if (y & 2**z) != 0])

def sqrt(x, p):
  if p % 4 == 3:
    return power(x, (p + 1) / 4, p)
