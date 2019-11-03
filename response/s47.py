'''

$ python3 s47.py


'''

from Crypto.Hash import SHA1
from Crypto.Util.number import getPrime
from Crypto.Random.random import getrandbits
from Crypto.Random.random import randint
from math import log, ceil, floor
from base64 import b64encode as e64, b64decode as d64
from s40_aux import extended_gcd as eea, invmod

class KEY_PUB:
  def __init__(self, e, n):
    self.e = e, self.n = n

class Oracle_47:
  def __init__(self):
    self.m = b'kick it, CC'
#    self.m = e64(b'hello\n')
#    self.x = int.from_bytes(d64(b'aGVsbG8K'), 'big')
#    self.x = 105
    print('keypair generation...init')
    while True:
      try:
        print('  try')
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
#        print('n', self.n)
        break
      except ValueError:
        continue
    print('keypair gen...OK\n')
    print('n', self.n)
    print('p', self.p)
    print('q', self.q)
    print('d', self.d, end='\n\n')
    PS_len = 32 - 2 - 1 - len(self.m)
    PS = b''
    while len(PS) < PS_len:
      byte_add = getrandbits(8)
      if byte_add == 0:
        continue
      PS += byte_add.to_bytes(1, 'big')
    self.m = b'\x00' + b'\x02' + PS + b'\00' + self.m
    assert len(self.m) == 32
    self.x = int.from_bytes(self.m, 'big')
    self.QUERYCOUNT = 0

  def keypub(self):
    return self.e, self.n

  def challenge(self):
    print('Encrypting:', x_to_m(self.x))
    print('...from int:', self.x, end='\n\n')
    assert self.decrypt(self.encrypt(self.x)) == self.x
    return self.encrypt(self.x)

  def encrypt(self, m):
    return pow(m, self.e, self.n)

  def decrypt(self, c):
    return pow(c, self.d, self.n)

  # ? pkcs conformant
  def query(self, c):
    self.QUERYCOUNT += 1
    m = pow(c, self.d, self.n)
#    print('query:', c)
    if (m >= (2 << 240)) and (m <= ((3 << 240) - 1)):  # [2B, 3B - 1]
      return True
    else:
      return False

  def querycount(self):
    return self.QUERYCOUNT
  def getx(self):
    return self.x
    
def x_to_m(x):
#  return x.to_bytes(ceil(log(x, 2) / 8), 'big')
  return x.to_bytes(32, 'big')

def main():
  moggle = Oracle_47()
  e, n = moggle.keypub()
  c = moggle.challenge()
  print('Moggle\'s challenge: ' + str(c), end='\n\n')

  B = 2 << 239

  s = [1]
#  r = [2 * B, (3 * B) - 1]
  a = 2 * B
  b = (3 * B) - 1
  M = [2 * B, (3 * B) - 1]
  i = 1

# 2a start
  s_i_try = ceil(n / (3 * B))

  print('s_1 candidate start: ' + str(s_i_try))
  print('Searching...')
  while True:
    if moggle.query((c * pow(s_i_try, e, n)) % n):
      print('s_1', s_i_try)
      break
    s_i_try += 1

  ra = ceil(((2 * B * s_i_try) - (3 * B) + 1) / n)
  rb = floor((((3 * B - 1) * s_i_try) - (2 * B)) / n)
  print('r in [', ra, ',', rb, ']')

  if ra != rb:
    print('multi r. panic.')
    exit(1)

  m0a = ceil(((2 * B) + (ra * n)) / s_i_try) % n
  m0b = floor((((3 * B) - 1) + (ra * n)) / s_i_try) % n
  print('m0 in... \n[\n  ' + str(m0a) + ', \n  ' + str(m0b) + '\n], modulo...\n  ' + str(n))
  print('vs\n  ' + str(2 * B) + ',\n  ' + str((3 * B) - 1), end='\n\n')
  if m0a > m0b:
    print('m0a m0b panic')
    exit(1)

  aa = ceil(((2 * B) + (ra * n)) / s_i_try) % n
  bb = floor((((3 * B) - 1) + (ra * n)) / s_i_try) % n

  M = [max(M[0], aa), min(M[1], bb)]
  print('new M:\n[\n  ' + str(M[0]) + ',\n  ' + str(M[1]) + '\n]\n')
  s_i_minus_1 = s_i_try

# START POWER LOOP
#  r_i = 0
  r_i = ceil(2 * (((M[1] * s_i_minus_1) - (2 * B)) / n)) - 1  # hi
  SUCCESSFUL = False
  while True:
    if not SUCCESSFUL:
      r_i += 1
    else:
      r_i = ceil(2 * (((M[1] * s_i_minus_1) - (2 * B)) / n))
    print('trying r =', r_i, end='')

    s_i_a = ceil(((2 * B) + (r_i * n)) / M[1])
    s_i_b = floor(((3 * B) + (r_i * n)) / M[0])

    SUCCESSFUL = False
    for s_i_try in range(s_i_a, s_i_b + 1):
      if moggle.query((c * pow(s_i_try, e, n)) % n):
        print('\n  s_i found at:', s_i_try)
        s_i = s_i_try
        SUCCESSFUL = True
        break
      print('.', end='')

    if not SUCCESSFUL:
      print('  s_i_try reached upper bound', s_i_b, ', increment r_i and try again')
      continue

    aa = ceil(((2 * B) + (r_i * n)) / s_i) % n
    bb = floor((((3 * B) - 1) + (r_i * n)) / s_i) % n

    s_i_minus_1 = s_i
    M = [max(M[0], aa), min(M[1], bb)]
    print('new M:\n[\n  ' + str(M[0]) + ',\n  ' + str(M[1]) + '\n]\n')
    if M[0] == M[1]:
      print('found m0:', M[0])
      print('decoded:', (M[0]).to_bytes(32, 'big'))
      break
    elif M[0] > M[1]:
      print('bounds crossed. panic')
      exit(1)





  print('oracle queried', moggle.querycount(),'times')
  print('oracle x:\n', moggle.getx())
  print(x_to_m(moggle.getx()))



if __name__ == '__main__':
  main()

