from Crypto.Util.number import getPrime
from Crypto.Random.random import getrandbits
from math import ceil, floor
from s40_aux import extended_gcd as eea, invmod

class O47:
  def __init__(self):
    self.m_original = b'kick it, CC'
    print('generating keypair...')
    while True:
      try:
        print('  try')
        self.p = getPrime(128)
        self.q = getPrime(128)
        if self.p == self.q:
          continue
        self.n = self.p * self.q
        self.et = (self.p - 1) * (self.q - 1)
        self.e = 3
#        self.e = 65537
        g, s, t = eea(self.e, self.et)
        self.d = invmod(self.e, self.et)
        break
      except ValueError:
        continue
    print('keypair gen...OK.\n')
    PS_len = 32 - 3 - len(self.m_original)
    PS = b''
    while len(PS) < PS_len:
      next_byte = getrandbits(8).to_bytes(1, 'big')
      if next_byte == b'\x00':
        continue
      PS += next_byte
    self.m = b'\x00\x02' + PS + b'\x00' + self.m_original
    print('p: ' + str(self.p))
    print('q: ' + str(self.q))
    print('n: ' + str(self.n))
    print('e: ' + str(self.e))
    print('d: ' + str(self.d))
    print('m:', self.m)
    print('P: ' + str(int.from_bytes(self.m, 'big')))

  def pubkey(self):
    return self.e, self.n

  def challenge(self):
    return pow(int.from_bytes(self.m, 'big'), self.e, self.n)

  def query(self, c):
    B = 2 << 239
    x = pow(c, self.d, self.n)
    if (x >= (2 * B)) and (x <= ((3 * B) - 1)):
      return True
    else:
      return False

def x_to_m(x):
  return (x).to_bytes(32, 'big')

def main():
  moggle = O47()
  e, n = moggle.pubkey()
  c = moggle.challenge()
  print('\nMoggle\'s challenge:\nc: ' + str(c), end='\n\n')

  B = 2 << 239
  a = 2 * B
  b = (3 * B) - 1
  M = [a, b]

  s_i = ceil(n / (3 * B))
  while True:
    if moggle.query(c * pow(s_i, e, n)):
      print('s1: ' + str(s_i))
      break
    s_i += 1

  ra = ceil(((M[0] * s_i) - (3 * B) + 1) / n)
  rb = floor((M[1] * s_i) / n)
  print('r in: [' + str(ra) + ', ' + str(rb) + ']\n')
  if ra != rb:
    print('multi-r. panic.')
    exit(1)

  aa = ceil((a + (ra * n)) / s_i)
  bb = floor((b + (ra * n)) / s_i)
  print('M0:\n[\n  ' + str(M[0]) + ',\n  ' + str(M[1]) + '\n]\n')
  M = [max(M[0], aa), min(M[1], bb)]
  print('M:\n[\n  ' + str(M[0]) + ',\n  ' + str(M[1]) + '\n]\n')
  s_i_last = s_i

  r_i = ceil(2 * (((M[1] * s_i_last) - a) / n)) - 1
  S_I_FOUND = False
  while True:
    if S_I_FOUND:
      r_i = ceil(2 * (((M[1] * s_i_last) - a) / n)) - 1
    else:
      r_i += 1
    print('trying r_i:', r_i)

    s_i_a = ceil((a + (r_i * n)) / M[1])
    s_i_b = floor((b + 1 + (r_i * n)) / M[0])
    s_i = s_i_a
#    assert (s_i_b >= s_i_a)  # this assert actually fails sometimes
    S_I_FOUND = False
    while s_i <= s_i_b:
      if moggle.query((c * pow(s_i, e, n)) % n):
        S_I_FOUND = True
        print('s_i', s_i)
        break
      s_i += 1
    if not S_I_FOUND:
      continue

    aa = ceil((a + (r_i * n)) / s_i)
    bb = floor((b + (r_i * n)) / s_i)
    M = [max(M[0], aa), min(M[1], bb)]
    print('M:\n[\n  ' + str(M[0]) + ',\n  ' + str(M[1]) + '\n]\n')
    s_i_last = s_i
    if M[0] > M[1]:
      print('bounds crossed. panic.')
      exit(1)
    elif M[0] == M[1]:
      break

  print(M[0])
  print((M[0]).to_bytes(32, 'big'))
  print(moggle.m)
  print(int.from_bytes(moggle.m, 'big'))

if __name__ == '__main__':
  main()

