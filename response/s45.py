'''
$ python3 s45.py


'''

from binascii import unhexlify
import re
from Crypto.Hash import SHA1
from Crypto.Random.random import randint
from s40_aux import invmod

class DataWrap:
  def __init__(self, msg, s, r, m):
    self.msg, self.s, self.r, self.m = msg, s, r, m

p_def = 0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1
q_def = 0xf4f47f05794b256174bba6e9b396a7707e563c5b
g_def = 0x5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291
g1 = 0
g2 = p_def + 1
B_def = 0x2d026f4bf30195ede3a088da85e398ef869611d0f68f0713d51c9c1a3a26c95105d915e2d8cdf26d056b86b8a7b85519b1c23cc3ecdc6062650462e3063bd179c2a6581519f674a61f1d89a1fff27171ebc1b93d4dc57bceb7ae2430f98a6a4d83d8279ee65d71c1203d2c96d65ebbf7cce9d32971c3de5084cce04a2e147821

class K_PUB:
  def __init__(self, p, q, g, B):
    self.p, self.q, self.g, self.B = p, q, g, B

# 43 PARAMETER!
#B = 0x84ad4719d044495496a3201c8ff484feb45b962e7302e56a392aee4abab3e4bdebf2955b4736012f21a08084056b19bcd7fee56048e004e44984e2f411788efdc837a0d2e5abb7b555039fd243ac01f0fb2ed1dec568280ce678e931868d23eb095fde9d3779191b8c0299d6e07bbb283e6633451e535c45513b2d33c99ea17

class DSA_45:
  def __init__(self, pk, d = 1379952329417023174824742221952501647027600451162):
    if pk.p is None:
      p_init = p_def
    else:
      p_init = pk.p
    if pk.q is None:
      q_init = q_def
    else:
      q_init = pk.q
    if pk.g is None:
      g_init = g_def
    else:
      g_init = pk.g
    if d is None:
      self.d = randint(2, q_init - 1)
    else:
      self.d = d
    if pk.B is None:
      B_init = pow(g_init, self.d, p_init)
    self.keypub = K_PUB(p_init, q_init, g_init, B_init)
#    print('key', self.d)
#    print('init g', hex(G))

  def sign(self, x, k_ephemeral):
    r = pow(self.keypub.g, k_ephemeral, self.keypub.p) % self.keypub.q
    mhash_intified = int.from_bytes(SHA1.new(x.encode()).digest(), 'big')
    s = ((mhash_intified + ((self.d * r))) * invmod(k_ephemeral, self.keypub.q)) % self.keypub.q
    return r, s

def verify(x, r, s, kpub):
  w = invmod(s, kpub.q)
  u1 = (w * int.from_bytes(SHA1.new(x.encode()).digest(), 'big')) % kpub.q
  u2 = (w * r) % kpub.q
  v = ((pow(kpub.g, u1, kpub.p) * pow(kpub.B, u2, kpub.p)) % kpub.p) % kpub.q
#  if kpub.g % kpub.p == 1:
#    print('term1', pow(kpub.g, u1, kpub.p), 'term2', pow(kpub.B, u2, kpub.p))
#    print('v is', v)
  if v == (r % kpub.q):
    return True
  else:
    return False

if __name__ == '__main__':

  m1 = 'For those that envy a MC it can be hazardous to your health\nSo be friendly, a matter of life and death, just like a etch-a-sketch\n'

# g = 0
  my = DSA_45(pk = K_PUB(None, None, g1, None))
  r, s = my.sign(m1, 16575)
#  print('r,s',r, s)
  if verify(m1, r, s, kpub = my.keypub):
    print('g = 0 sign and verify. sanity check PASS')

# g = 0, cont'd.
# Arbitrary m, regardless of (r, s)
  if verify('Hello, world', r, s, kpub = my.keypub):
    print('uh-oh.')
  if verify('Goodbye, world', r, s, kpub = my.keypub):
    print('uh-oh.')

# g = p + 1
  print('\n\n')
  my = DSA_45(d = None, pk = K_PUB(None, None, g2, None))
  r, s = my.sign(m1, 16575)
  print('r, s', r, s)
  if verify(m1, r, s, kpub = my.keypub):
    print('g = p + 1 sign and verify. sanity check PASS')
  else:
    print('wtf mate')
  print('\n\n')

  z = randint(2, my.keypub.q - 1)
  r = pow(g2, z, my.keypub.p) % my.keypub.q
  s = (r * invmod(z, my.keypub.q)) % my.keypub.q

  if verify('Hello, world', r, s, my.keypub):
    print('uh-oh2.')
  else:
    print('not yet2')
  if verify('Goodbye, world', r, s, my.keypub):
    print('uh-oh2.')
  else:
    print('not yet2')

