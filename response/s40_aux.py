
from Crypto.Util.number import getPrime
from decimal import Decimal, getcontext

# Pulled from Rosetta Code
def eratosthenes2(n):
  multiples = set()
  for i in range(2, n+1):
    if i not in multiples:
      yield i
      multiples.update(range(i*i, n+1, i))

# Pulled from Rosetta Code
def extended_gcd(aa, bb):
  lastremainder, remainder = abs(aa), abs(bb)
  x, lastx, y, lasty = 0, 1, 1, 0
  while remainder:
    lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
    x, lastx = lastx - quotient*x, x
    y, lasty = lasty - quotient*y, y
  return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

# Pulled from Rosetta Code
def invmod(a, m):
  g, x, y = extended_gcd(a, m)
  if g != 1:
    raise ValueError
  return x % m

# Pulled from Rosetta Code
def nthroot (n, A, precision):
  getcontext().prec = precision

  n = Decimal(n)
  x_0 = A / n #step 1: make a while guess.
  x_1 = 1     #need it to exist before step 2
  while True:
    x_0, x_1 = x_1, (1 / n)*((n - 1)*x_0 + (A / (x_0 ** (n - 1))))
    if x_0 == x_1:
      return x_1

