'''
$ python3 s41.py

'''
from Crypto.Util.number import getPrime
from Crypto.Random.random import randint
from Crypto.Hash import SHA256
from math import log, ceil
import json
from s40_aux import extended_gcd as eea, invmod

class Oracle_41:
  def __init__(self):
    data = {'time': 1356304276, 'social': '555-55-5555'}
    self.message = json.JSONEncoder().encode(data)
    x = int.from_bytes(self.message.encode(), 'big')
    self.p = getPrime(512)
    while True:
      self.q = getPrime(512)
      if self.q != self.p:
        break
    self.n = self.p * self.q
    self.et = (self.p - 1) * (self.q - 1)
    while True:
      print('try')
      self.e = randint(2, self.et - 1)
      g, s, t = eea(self.e, self.et)
      if g == 1:
        break
    self.d = invmod(self.e, self.et)
    c = pow(x, self.e, self.n)
    self.c_hash = SHA256.new(str(c).encode()).digest()

  def challenge(self):
    data_raw_dict = {'time': 1356304276, 'social': '555-55-5555'}
    message = json.JSONEncoder().encode(data_raw_dict)
    x = int.from_bytes(message.encode(), 'big')
    c = pow(x, self.e, self.n)
    return c, self.e, self.n

  def query(self, c):
    h = SHA256.new(str(c).encode()).digest()
    if h == self.c_hash:
      print('Dia: Still live..Bottom.\n')
    else:
      print('Dia: Shut up and take my plaintext!\n')
      return pow(c, self.d, self.n)

  def check_response(self, m):
    if m == self.message:
      return True
    else:
      return False

if __name__ == '__main__':
  Dia = Oracle_41()
  c, e, n = Dia.challenge()

  s = randint(2, n-1)
  cX = (pow(s, e, n) * c) % n

  print('Sending back challenge ciphertext.')
  garbo = Dia.query(c)
  print('Sending altered ciphertext.')
  pX = Dia.query(cX)

  p = pX * invmod(s, n) % n

  m = p.to_bytes((ceil(log(p, 2)/8)) , 'big')
  print('Sending response: ' + m.decode())
  if Dia.check_response(m.decode()):
    print('huzzah')
  else:
    print('kaboom')


