'''
Toy module thrown together during set 5 / challenge 40 as a study aid for:
  Garner, Harry L. “The Residue Number System.” 1959 Proceedings of the Western Joint Computer Conference.

Meant to be used as an '... import *' within the interpreter.

'''

def rns_enc(i):
  assert(type(i) is int)
  return [i%2, i%3, i%5, i%7]

def rns_dec(s):
  assert(type(s) is str)
  assert(len(s) is 4)
  assert(s[0] in '01')
  assert(s[1] in '012')
  assert(s[2] in '01234')
  assert(s[3] in '0123456')
  return dict2357[s]

def r2357_add(a, b):
  return rns_enc(rns_dec(a) + rns_dec(b))

def r2357_sub(a, b):
  return rns_enc(rns_dec(a) - rns_dec(b) % 210)

#def r2357_mul(a, b):

dict2357 = dict([(str(rns_enc(x)[0])+str(rns_enc(x)[1])+str(rns_enc(x)[2])+str(rns_enc(x)[3]), x) for x in range(210)])

# Rosetta Code
def extended_gcd(aa, bb):
  lastremainder, remainder = abs(aa), abs(bb)
  x, lastx, y, lasty = 0, 1, 1, 0
  while remainder:
    lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
    x, lastx = lastx - quotient*x, x
    y, lasty = lasty - quotient*y, y
  return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

# Rosetta Code 
def modinv(a, m):
  g, x, y = extended_gcd(a, m)
  if g != 1:
    raise ValueError
  return x % m

