'''
$ python3 s44.py


Derivation, at the problem description's request:

  Given: s = (m + d*r) * invmod(k_eph)

s1 - s2 = ((m1 + d*r) * invmod(k_eph)) - ((m2 + d*r) * invmod(k_eph))
        = (        (m1 + d*r) - (m2 + d*r)         ) * invmod(k_eph)
        = (m1 + d*r - m2 - d*r) * invmod(k_eph)
        = (m1 - m2) * invmod(k_eph)
      <==>
  k_eph = (m1 - m2) * invmod(s1 - s2)

'''

from binascii import unhexlify
import re
from Crypto.Hash import SHA1
from s40_aux import invmod

challenge = 'ca8f6f7c66fa362d40760d135b763eb8527d3d52'

class DataWrap:
  def __init__(self, msg, s, r, m):
    self.msg, self.s, self.r, self.m = msg, s, r, m

p = 0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1
q = 0xf4f47f05794b256174bba6e9b396a7707e563c5b
g = 0x5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291
B = 0x2d026f4bf30195ede3a088da85e398ef869611d0f68f0713d51c9c1a3a26c95105d915e2d8cdf26d056b86b8a7b85519b1c23cc3ecdc6062650462e3063bd179c2a6581519f674a61f1d89a1fff27171ebc1b93d4dc57bceb7ae2430f98a6a4d83d8279ee65d71c1203d2c96d65ebbf7cce9d32971c3de5084cce04a2e147821

# 43 PARAMETER!
#B = 0x84ad4719d044495496a3201c8ff484feb45b962e7302e56a392aee4abab3e4bdebf2955b4736012f21a08084056b19bcd7fee56048e004e44984e2f411788efdc837a0d2e5abb7b555039fd243ac01f0fb2ed1dec568280ce678e931868d23eb095fde9d3779191b8c0299d6e07bbb283e6633451e535c45513b2d33c99ea17
class Entity_44:
  def __init__(self, d = 125489817134406768603130881762531825565433175625):
    self.d = d
  def sign(self, x, k_ephemeral):
    r = pow(g, k_ephemeral, p) % q
    mhash_intified = int.from_bytes(SHA1.new(x.encode()).digest(), 'big')
    s = ((mhash_intified + ((self.d * r))) * invmod(k_ephemeral, q)) % q
    return r, s

def verify(x, r, s):
  w = invmod(s, q)
  u1 = (w * int.from_bytes(SHA1.new(x.encode()).digest(), 'big')) % q
  u2 = (w * r) % q
  v = ((pow(g, u1, p) * pow(B, u2, p)) % p) % q
  if v == (r % q):
    return True
  else:
    return False

if __name__ == '__main__':
  lines = list(open('challenge/44.txt', 'r').readlines())

  data = []
  i = 0
  for line in lines:
    if i % 4 == 0:
      hit = re.search(r'^msg: ', line)
      msg = line[hit.end():-1]
    elif i % 4 == 1:
      hit = re.search(r'^s: ', line)
      s = int(line.strip()[hit.end():])
    elif i % 4 == 2:
      hit = re.search(r'^r: ', line)
      r = int(line.strip()[hit.end():])
    elif i % 4 == 3:
      hit = re.search(r'^m: ', line)
      if len(line.strip()[hit.end():]) % 2 == 0:
        m = line.strip()[hit.end():]
      else:
        m = '0' + line.strip()[hit.end():]
    i += 1
    if i % 4 == 0:
      data.append(DataWrap(msg, s, r, m))

# Verify proper data import
  for line in data:
    print(str(type(line.msg)) + ' ' + line.msg + '\n  ' + str(type(line.s)) + ' ' + str(line.s) + '\n  ' + str(type(line.r)) + ' ' + str(line.r) + '\n  ' + str(type(line.m)) + ' ' + line.m)
    assert(SHA1.new(line.msg.encode()).hexdigest() == line.m)
    if verify(line.msg, line.r, line.s):
      print('VERIFY OK\n')
    else:
      print('eek!')
      exit()

# This code block only works if the alternate B parameter is toggled at the top of this src

#  m43 = 'For those that envy a MC it can be hazardous to your health\nSo be friendly, a matter of life and death, just like a etch-a-sketch\n'
#  test43 = Entity_44()
#  r43, s43 = test43.sign(m43, 16575)
#  print('r=', r43, '\ns=', s43)
#  print(type(r43), type(s43))
#  if pow(g, 16575, p) % q == r43:
#    print('eph ok')
#  else:
#    print('eph panic')
#    exit()
#  if verify(m43, r43, s43):
#    print('okay!')
#  else:
#    print('panic!')
#    exit()

  for i in range(len(data) - 1):
    for j in range(i + 1, len(data)):
      m1 = int.from_bytes(unhexlify(data[i].m.encode()), 'big')
      m2 = int.from_bytes(unhexlify(data[j].m.encode()), 'big')
      s_inv = invmod(((data[i].s - data[j].s) % q), q)
      k_ephemeral_candidate = (((m1 - m2) % q) * s_inv) % q

      d_candy = (((data[i].s * k_ephemeral_candidate) - int.from_bytes(unhexlify(data[i].m.encode()), 'big')) * invmod(data[i].r, q)) % q
      gal = Entity_44(d_candy)
      try:
        r_, s_ = gal.sign(data[i].msg, k_ephemeral_candidate)
        if s_ == data[i].s:
          print('probable key ' + str(d_candy) + ' from i=' + str(i) + ' and j=' + str(j))
          if SHA1.new(hex(d_candy)[2:].encode()).hexdigest() == challenge:
            print('huzzah')
            exit(0)
          else:
            print('unexpected')
#        else:
#          print('no dice ' + str(d_candy))
      except ValueError:
#        print('exception from i=' + str(i) + ' and j=' + str(j))
        pass

