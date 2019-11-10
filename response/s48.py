from Crypto.Util.number import getPrime
from Crypto.Random.random import getrandbits
import intervals as I
from math import ceil, floor
#from time import sleep

# TOGGLE
B = 2 << 239  # 256-bit modulus
#B = 2 << 751  # 768-bit modulus

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
        self.p = getPrime(128)
        self.q = getPrime(128)
#        self.p = getPrime(384)
#        self.q = getPrime(384)
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
    PS_len = 32 - 3 - len(self.m_original)
#    PS_len = 96 - 3 - len(self.m_original)
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
    B = 2 << 239
#    B = 2 << 751
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
  numerator = (a * s_i) - ((3 * B) - 1)
  return ceil(numerator / n)

def s3_calc_rb(b, s_i, n):
  numerator = (b * s_i) - (2 * B)
  return floor(numerator / n)

# calculate INNER(!) comparison bounds for condition (3)
def s3_calc_aa(r, n, s_i):
  numerator = (2 * B) + (r * n)
  return ceil(numerator / s_i)

def s3_calc_bb(r, n, s_i):
  numerator = (3 * B) - 1 + (r * n)
  return floor(numerator / s_i)

# calculate s_i bounds for condition (2)
def step_2c_calc_sa(r, n, b):
  numerator = (2 * B) + (r * n)
  return ceil(numerator / b)

def step_2c_calc_sb(r, n, a):
  numerator = (3 * B) + (r * n)
  return floor(numerator / a)




def main():
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
    if moggle.query(c * pow(s_i, e, n)):
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
    bbb = min(M_last[0][1], bb)
    m_i |= I.closed(aaa, bbb)
  I_last = I_last & m_i
  M = []
  for interval in I.to_data(m_i):
    M.append([interval[1], interval[2]])
#  print('\n')
#  for line in M:
#    print(line)

  s_i_last = s_i
  M_last = M


#  exit(0)
# step2 2nd iteration start
#   and step 3
  while len(M_last) > 1:
    s_i += 1
#    print('  multi-I, s_i = ' + str(s_i))
    if not moggle.query((c * pow(s_i, e, n)) % n):
      continue
    else:
      # are all these r-vals guaranteed to be oracle hits?
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

  print('checkpoint')
  for line in M:
    print('[\n  ' + str(line[0]) + ',\n  ' + str(line[1]) + '\n]\n')
# start 2c, one interval left

  try:
    print('\n\nphase single-I start\n')
    S_I_FOUND = False
    r_i = ceil(2 * (((M_last[0][1] * s_i_last) - (2 * B)) / n)) - 1
    while True:
      if S_I_FOUND:
        r_i = ceil(2 * (((M_last[0][1] * s_i_last) - (2 * B)) / n))
      else:
        r_i += 1

      sa = step_2c_calc_sa(r_i, n, M_last[0][1])
      sb = step_2c_calc_sb(r_i, n, M_last[0][0])
#      print('r_i:', r_i, '// si search range:[', sa, ',', sb, ']', '// last s_i', s_i_last, '  calculated from interval\n[\n  ', M_last[0][0], ',\n  ', M_last[0][1], ']\n')
      print('r_i:', r_i, '// si search range:[', sa, ',', sb, ']', '// last s_i', s_i_last, '\n')

      if sa > sb + 1:
        print('single-I s_i bounding panic.')
        print(M_last[0][0])
        print(M_last[0][1])
        exit(1)
      elif sa > sb:
        sb = sa + 1
      S_I_FOUND = False
      for si in range(sa, sb + 1):
        if moggle.query((c * pow(si, e, n)) % n):
          S_I_FOUND = True
          print('  HIT:  si = ' + str(si))
          s_i = si
#          m_i = I.empty()
          aa = s3_calc_aa(r_i, n, s_i)
          bb = s3_calc_bb(r_i, n, s_i)
          if (aa > b) or (bb < a):
            print('    out of bounds. break.')
            s_i_last = s_i
            break
          aaa = max(M_last[0][0], aa)
          bbb = min(M_last[0][1], bb)
          m_i = I.closed(aaa, bbb)
          break
      if not S_I_FOUND:
#        s_i_last = s_i # ??
        continue
      I_last = I_last & m_i

      s_i_last = s_i
      M = []
      for interval in I.to_data(I_last):
        M.append([interval[1], interval[2]])
        print('       s_i = ' + str(s_i) + '\n    [\n      ' + str(interval[1]) + '\n      ' + str(interval[2]) + '\n    ]\n')
      M_last = M
      if len(M_last) > 1:
        print('interval count re-multiplied. panic.')
        exit(1)
      if M_last[0][0] == M_last[0][1]:
        break
  except KeyboardInterrupt:
    print('\ncrack')
# TOGGLE
    print((M[0][0]).to_bytes(32, 'big'), end='\n\n')
#    print((M[0][0]).to_bytes(96, 'big'), end='\n\n')
    print(M[0][0])

    print('oracle')
    print(moggle.m)
    print(int.from_bytes(moggle.m, 'big'))
    print('\nqueried ' + str(moggle.qcount()) + ' times')
    print('true ' + str(moggle.tcount()) + ' times')


  print('crack')
  print(M[0][0])
# TOGGLE
  print((M[0][0]).to_bytes(32, 'big'), end='\n\n')
#  print((M[0][0]).to_bytes(96, 'big'), end='\n\n')

  print('oracle')
  print(moggle.m)
  print(int.from_bytes(moggle.m, 'big'))
  print('\nqueried ' + str(moggle.qcount()) + ' times')
  print('true ' + str(moggle.tcount()) + ' times')

if __name__ == '__main__':
  main()
