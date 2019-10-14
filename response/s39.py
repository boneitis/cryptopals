'''
$ python3 s39.py


'''

from Crypto.Random.random import sample
from Crypto.Util.number import getPrime
#from Crypto.Random.random import randint

'''
# Pulled from Rosetta Code
def eratosthenes2(n):
  multiples = set()
  for i in range(2, n+1):
    if i not in multiples:
      yield i
      multiples.update(range(i*i, n+1, i))
'''

def eea(r0, r1):
  if r0 > r1:
    r = [r0, r1]
  elif r1 < r0:
    r = [r1, r0]
  else:
    return r0

  s = [1, 0]
  t = [0, 1]
  i = 1

  while r[i] != 0:
    i += 1
    r.append(r[i-2] % r[i-1])
    q = (r[i-2]-r[i]) // r[i-1]    
    s.append(s[i-2] - (q * s[i-1]))
    t.append(t[i-2] - (q * t[i-1]))

  return r[i-1], s[i-1], t[i-1]

def invmod(a, m):
  g, s, t = eea(m, a)
#  print('INVMOD: Passed m, a', m, a, 'returned g', g)
  if g != 1:
#    pass
    raise ValueError
  return t % m

'''
# Pulled from Rosetta Code
def extended_gcd(aa, bb):
  lastremainder, remainder = abs(aa), abs(bb)
  x, lastx, y, lasty = 0, 1, 1, 0
  while remainder:
    lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
    x, lastx = lastx - quotient*x, x
    y, lasty = lasty - quotient*y, y
  return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def invmod(a, m):
  g, x, y = extended_gcd(a, m)
  if g != 1:
    raise ValueError
  return x % m

'''

def main():
#  primes100_choose_2 = sample(list(eratosthenes2(100)), 2)
#  p = primes100_choose_2[0]
#  q = primes100_choose_2[1]

  done = False
  while not done:
    try:
      p = getPrime(512)
      while True:
        q = getPrime(512)
        if q != p:
          break

      n = p * q
      et = (p - 1) * (q - 1)
#      e = randint(1, et - 1)
      e = 3
      g, s, t = eea(et, e)
      print(g)
      if g != 1:
        continue

#  gcd, s, t = eea(973, 301)
#  print(gcd, s, t)             # 7 13 -42
#  gcd, s, t = eea(243, 198)
#  print(gcd, s, t)             # 9 9 -11
#  gcd, s, t = eea(3587, 1819)
#  print(gcd, s, t)             # 17 -36 71
#  inv = invmod(42, 2017)
#  print(inv)                   # 1969
#  inv = invmod(17, 3120)
#  print(inv)                   # 2753

      d = invmod(e, et)

#      m = 42
      m = b"I'm killing your brain like a poisonous mushroom"
      m_encode = int.from_bytes(m, 'big')
      c = pow(m_encode, e, n)
      m_1 = pow(c, d, n).to_bytes(128, 'big')

      if m == m_1[-48:]:
        print(m_1[-48:].decode())
        done = True
    except ValueError:
      pass

if __name__ == '__main__':
  main()

