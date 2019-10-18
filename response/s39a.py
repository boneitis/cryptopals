
from Crypto.Util.number import getPrime

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

