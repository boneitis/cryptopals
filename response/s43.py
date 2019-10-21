'''
$ python3 s43.py

ToDo: Grok the math.

'''

from binascii import unhexlify
from Crypto.Hash import SHA1
from Crypto.Random.random import randint
from s40_aux import extended_gcd as eea, invmod

class K_PUB:
  def __init__(self, p, q, g, B):
    self.p, self.q, self.g, self.B = p, q, g, B

class Entity_43:
  def __init__(self):
    p = int.from_bytes(unhexlify(b'800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1'), 'big')
    q = int.from_bytes(unhexlify(b'f4f47f05794b256174bba6e9b396a7707e563c5b'), 'big')
    g = int.from_bytes(unhexlify(b'5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291'), 'big')
    d = randint(2, q - 1)
    B = pow(g, d, p)
    self.k_pub = K_PUB(p, q, g, B)
    self.b = d
    self.x = b'For those that envy a MC it can be hazardous to your health\nSo be friendly, a matter of life and death, just like a etch-a-sketch\n'

  def sign(self, x):
    while True:
      print('try')
      k_ephemeral = randint(2, self.k_pub.q - 1)
      remainder, _, _ = eea(k_ephemeral, self.k_pub.p - 1)
      if remainder == 1:
        break
    r = pow(self.k_pub.g, k_ephemeral, self.k_pub.p) % self.k_pub.q
    mhash_intified = int.from_bytes(SHA1.new(x).digest(), 'big')
    s = ((mhash_intified + (self.b * r)) * invmod(k_ephemeral, self.k_pub.q)) % self.k_pub.q
    return r, s

def verify(x, r, s, k):
  print('in verify', k.p, '\n', k.g, '\n', k.q, '\n', k.B, '\n')
  w = invmod(s, k.q)
  mhash_intified = int.from_bytes(SHA1.new(x).digest(), 'big')
  u_1 = (w * mhash_intified) % k.q
  u_2 = (w * r) % k.q
  v = ((pow(k.g, u_1, k.p) * pow(k.B, u_2, k.p)) % k.p) % k.q
  print('term1', pow(k.g, u_1, k.p), end='\n\n')
  print('term2', pow(k.B, u_2, k.p), end='\n\n')
  print('v', v)
  print('r', r)
  if v == r % k.q:
    return True
  else:
    return False

if __name__ == '__main__':
  gal = Entity_43()
  r, s = gal.sign(gal.x)
  print(r, s)
  if verify(b'For those that envy a MC it can be hazardous to your health\nSo be friendly, a matter of life and death, just like a etch-a-sketch\n', r, s, gal.k_pub):
    print('True')
  else:
    print('False')

  print('\nproblem description params')
  r = 548099063082341131477253921760299949438196259240
  s = 857042759984254168557880549501802188789837994940
  s_target = '0954edd5e0afe5542a4adf012611a91912a3ec16'
  for i in range(2**16 - 1):
    print(i)
    gal = Entity_43(i)
    r, s = gal.sign(gal.x)
    if s == 857042759984254168557880549501802188789837994940:
      print('match at i = ' + str(i))
      break

