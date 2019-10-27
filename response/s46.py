from Crypto.Hash import SHA1
from Crypto.Util.number import getPrime
from math import log, ceil
from base64 import b64encode as e64, b64decode as d64
from s40_aux import extended_gcd as eea, invmod

class Oracle_46:
  def __init__(self):
#    self.m = b'VGhhdCdzIHdoeSBJIGZvdW5kIHlvdSBkb24ndCBwbGF5IGFyb3VuZCB3aXRoIHRoZSBGdW5reSBDb2xkIE1lZGluYQ=='
    self.m = b'aGVsbG8K'
#    self.x = int.from_bytes(d64(b'aGVsbG8K'), 'big')
    self.x = 105
    while True:
      try:
        print('try')
        self.p = getPrime(512)
        self.q = getPrime(512)
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
    lsb = pow(c, self.d, self.n) & 0b1
    if lsb == 0b1:
      return True
    else:
      return False
    
def x_to_m(x):
  return x.to_bytes(ceil(log(x, 2) / 8), 'big')

if __name__ == '__main__':
  l = Oracle_46()
  c = lani.challenge()
  print(c)

  lower = 0
  upper = lani.n - 1
  for i in range(1024):
    if l.query(8 * c):

