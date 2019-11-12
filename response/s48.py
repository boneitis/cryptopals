'''
$ python3 s48.py


'''

from Crypto.Util.number import getPrime
from Crypto.Random.random import getrandbits
import intervals as I
from math import ceil, floor
from decimal import *

# TOGGLE
#B = 2 << 239  # 256-bit modulus
B = 2 << 751  # 768-bit modulus

# Pulled from Rosetta Code
def eea(aa, bb):
  lastremainder, remainder = abs(aa), abs(bb)
  x, lastx, y, lasty = 0, 1, 1, 0
  while remainder:
    lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
    x, lastx = lastx - quotient*x, x
    y, lasty = lasty - quotient*y, y
  return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

# Pulled from Rosetta Code
def invmod(a, m):
  g, x, y = eea(a, m)
  if g != 1:
    raise ValueError
  return x % m

class O47:
  def __init__(self):
    self.m_original = b'kick it, CC'
    print('generating keypair...')
    while True:
      try:
        print('  try')
# TOGGLE
#        self.p = getPrime(128)
#        self.q = getPrime(128)
        self.p = getPrime(384)
        self.q = getPrime(384)
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
    print('key gen OK.\n')
# TOGGLE
#    PS_len = 32 - 3 - len(self.m_original)
    PS_len = 96 - 3 - len(self.m_original)
    PS = b''
    while len(PS) < PS_len:
      next_byte = getrandbits(8).to_bytes(1, 'big')
      if next_byte == b'\x00':
        continue
      PS += next_byte
    self.m = b'\x00\x02' + PS + b'\x00' + self.m_original
    self.querycount = 0
    self.truecount = 0
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
    self.querycount += 1
# TOGGLE
#    B = 2 << 239
    B = 2 << 751
    x = pow(c, self.d, self.n)
    if (x >= (2 * B)) and (x <= ((3 * B) - 1)):
      self.truecount += 1
      return True
    else:
      return False

  def qcount(self):
    return self.querycount

  def tcount(self):
    return self.truecount

# calculate r bounds underneath condition (3)
def s3_calc_ra(a, s_i, n):
  numerator = (Decimal(a) * Decimal(s_i)) - Decimal((3 * B) - 1)
  return ceil(numerator / Decimal(n))

def s3_calc_rb(b, s_i, n):
  numerator = Decimal(b * s_i) - Decimal(2 * B)
  return floor(numerator / Decimal(n))

# calculate INNER(!) comparison bounds for condition (3)
def s3_calc_aa(r, n, s_i):
  numerator = Decimal(2 * B) + Decimal(r * n)
  return ceil(numerator / Decimal(s_i))

def s3_calc_bb(r, n, s_i):
  numerator = Decimal(3 * B) - Decimal(1) + Decimal(r * n)
  return floor(numerator / Decimal(s_i))

# step 2c, condition (1)
def step_2c_calc_ri_start(b, s_i_last, n):
  numerator = Decimal(b * s_i_last) - Decimal(2 * B)
  return ceil(Decimal(2 * (numerator / Decimal(n))))

# calculate s_i bounds, condition (2)
def step_2c_calc_sa(r, n, b):
  numerator = Decimal(2 * B) + Decimal(r * n)
  return ceil(numerator / Decimal(b))

def step_2c_calc_sb(r, n, a):
  numerator = Decimal(3 * B) + Decimal(r * n)
  return ceil(numerator / Decimal(a))




def main():
  getcontext().prec = 8192
  moggle = O47()
  e, n = moggle.pubkey()
  c = moggle.challenge()
  print('\nMoggle\'s challenge:\nc: ' + str(c), end='\n\n')

  a = 2 * B
  b = (3 * B) - 1
  M_last = [[a, b]]
  I_last = I.closed(a, b)

  s_i = ceil(n / (3 * B))
  while True:
    if moggle.query((c * pow(s_i, e, n)) % n):
      print('s1: ' + str(s_i))
      break
    s_i += 1

  ra = s3_calc_ra(M_last[0][0], s_i, n)
  rb = s3_calc_rb(M_last[0][1], s_i, n)
  print('r in: [' + str(ra) + ', ' + str(rb) + ']\n')
  r_i = [ra, rb]
  if ra > rb:
    print('r-val panic.')
    exit(1)


  m_i = I.empty()
  for little_r in range(ra, rb + 1):
    aa = s3_calc_aa(little_r, n, s_i)
    bb = s3_calc_bb(little_r, n, s_i)
    if (aa > b) or (bb < a):
      print('bad interval. continue.')
      continue
    aaa = max(M_last[0][0], aa)
    bbb = min(M_last[len(M_last) - 1][1], bb)
    m_i |= I.closed(aaa, bbb)
  I_last = I_last & m_i
  M = []
  for interval in I.to_data(m_i):
    M.append([interval[1], interval[2]])

  s_i_last = s_i
  M_last = M

# step2 2nd iteration start
#   and step 3
  while len(M_last) > 1:
    s_i += 1
#    print('  multi-I, s_i = ' + str(s_i))
    if not moggle.query((c * pow(s_i, e, n)) % n):
      continue
    else:
      m_i = I.empty()
      ra = s3_calc_ra(M[0][0], s_i, n)
      rb = s3_calc_rb(M[len(M) - 1][1], s_i, n)
      if ra > rb:
        print('multi-I r-val panic.')
        exit(1)
      for little_r in range(ra, rb + 1):
        for little_interval in M_last:
          aa = s3_calc_aa(little_r, n, s_i)
          bb = s3_calc_bb(little_r, n, s_i)
          aaa = max(little_interval[0], aa)
          bbb = min(little_interval[1], bb)
          m_i |= I.closed(aaa, bbb)
      I_last = I_last & m_i
      M = []
      for interval in I.to_data(I_last):
        M.append([interval[1], interval[2]])
        print('  s_i: ' + str(s_i) + '\n    [\n      ' + str(interval[1]) + '\n      ' + str(interval[2]) + '\n    ]\n')
      M_last = M
      s_i_last = s_i

  M_last = M[0]
  print('checkpoint')
  print('[\n  ' + str(M_last[0]) + ',\n  ' + str(M_last[1]) + '\n]\n')
# start 2c, one interval left

  try:
    print('\n\nphase single-I start\n')
    S_I_FOUND = False
    r_i = step_2c_calc_ri_start(M_last[1], s_i_last, n) - 1
    while True:
      if S_I_FOUND:
        r_i = step_2c_calc_ri_start(M_last[1], s_i_last, n)
      else:
        r_i += 1
#      print('  r_i', r_i)
      sa = step_2c_calc_sa(r_i, n, M_last[1])
      sb = step_2c_calc_sb(r_i, n, M_last[0])
      si = sa
      S_I_FOUND = False
#      print('    si:[', sa, ',', sb, ']')
      while True:
        if moggle.query((c * pow(si, e, n)) % n):
          S_I_FOUND = True
          s_i = si
          break
        si += 1
        if si > sb: # this should only trigger if no conformant s_i was found ; increment r_i and start over
          break
      if not S_I_FOUND: # remainder of try block should only execute if a conformant s_i was found
        continue
#      print('    s_i', s_i) ####

      aa = s3_calc_aa(r_i, n, s_i)
      bb = s3_calc_bb(r_i, n, s_i)
      aaa = max(M_last[0], aa)
      bbb = min(M_last[1], bb)
      m_i = I.closed(aaa, bbb)
#      print('aa\n', aa, '\nbb\n', bb)
#      print('m_i\n',aaa,'\n',bbb,end='\n\n')

      I_last = I_last & m_i
      if len(I_last) > 1:
        print('candidate intervals re-multiplied. panic.')
        exit(1)

      M_last = [I.to_data(I_last)[0][1], I.to_data(I_last)[0][2]]
#      print('  new M\n  [\n    ' + str(M_last[0]) + ',\n    ' + str(M_last[1]) + '\n  ]\n')
      if M_last[0] == M_last[1]:
        break
      s_i_last = s_i
      print((M_last[0]).to_bytes(96, 'big'))

  except KeyboardInterrupt:
    print('\n\n======================================\n\ncrack')
# TOGGLE
#    print((M_last[0]).to_bytes(32, 'big'))
    print((M_last[0]).to_bytes(96, 'big'))
    print(M_last[0])
    print(M_last[1], end='\n\n')

    print('oracle')
    print(moggle.m)
    print(int.from_bytes(moggle.m, 'big'))
    print('\nc', c)
    print('n', moggle.n)
    print('d', moggle.d)
    print('\nqueried ' + str(moggle.qcount()) + ' times')
    print('true ' + str(moggle.tcount()) + ' times')
    exit(1)


  print('\n\n======================================\n\ncrack')
# TOGGLE
#  print((M_last[0]).to_bytes(32, 'big'))
  print((M_last[0]).to_bytes(96, 'big'))
  print(M_last[0], end='\n\n')

  print('oracle')
  print(moggle.m)
  print(int.from_bytes(moggle.m, 'big'))
  print('\nc', c)
  print('d', moggle.d)
  print('n', moggle.n)
  print('\nqueried ' + str(moggle.qcount()) + ' times')
  print('true ' + str(moggle.tcount()) + ' times')

if __name__ == '__main__':
  main()
