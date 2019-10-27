'''

$ python3 s47.py


'''

from Crypto.Hash import SHA1
from Crypto.Util.number import getPrime
from Crypto.Random.random import getrandbits
from math import log, ceil
from base64 import b64encode as e64, b64decode as d64
from s40_aux import extended_gcd as eea, invmod

class Oracle_47:
  def __init__(self):
    self.m = b'kick it, CC'
#    self.m = e64(b'hello\n')
    self.x = int.from_bytes(d64(self.m), 'big')
#    self.x = int.from_bytes(d64(b'aGVsbG8K'), 'big')
#    self.x = 105
    while True:
      try:
        print('try')
        self.p = getPrime(128)
        self.q = getPrime(128)
        if self.q == self.p:
          continue
        self.n = self.p * self.q
        self.et = (self.p - 1) * (self.q - 1)
        self.e = 3
#        self.e = 65537
        g, s, t = eea(self.et, self.e) # will raise ValueError if gcd != 1
        self.d = invmod(self.e, self.et)
        break
      except ValueError:
        continue
    PS_len = 64 - 2 - 1 - len(self.m)
    PS = b''
    while len(PS) < PS_len:
      byte_add = getrandbits(8)
      if byte_add == 0:
        continue
      PS += byte_add.to_bytes(1, 'big')

  def keypub(self):
    return [self.e, self.n]

  def challenge(self):
    assert self.decrypt(self.encrypt(self.x)) == self.x
    return self.encrypt(self.x)

  def encrypt(self, m):
    return pow(m, self.e, self.n)

  def decrypt(self, c):
    return pow(c, self.d, self.n)

  # even or odd
  def query(self, c):
    m = x_to_m(pow(c, self.d, self.n))
    if m[0] == b'\x00' and m[1] == b'\x01': # [2B, 3B - 1], edit
      return True
    else:
      return False
    
def x_to_m(x):
  return x.to_bytes(ceil(log(x, 2) / 8), 'big')

if __name__ == '__main__':
  moggle = Oracle_47()
  c = moggle.challenge()
  print(c)
'''
  lower = 0
  upper = moggle.n - 1
  for i in range(256):
    print(x_to_m(upper))
    c *= 8
    if moggle.query(c):
      lower += (upper - lower) // 2
    else:
      upper -= (upper - lower) // 2
  print('\n')

  print(x_to_m(upper))
  print(x_to_m(lower))
'''

