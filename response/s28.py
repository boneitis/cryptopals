'''
$ python3 s28.py

'''

from Crypto.Util.strxor import strxor

class SHA1_28:
  def __init__(self):
    self.h0 = 0x67452301
    self.h1 = 0xEFCDAB89
    self.h2 = 0x98BADCFE
    self.h3 = 0x10325476
    self.h4 = 0xC3D2E1F0

  def preprocess(self, m):
    ml = len(m)
    m += b'\x80'
    padding = 448 - ((ml+1)%512)
    if padding < 0:
      padding += 512
    m += b'\x00' * padding
    return m

  def digest(self, m):
    m = self.preprocess(m)
    chunks = []
    for i in range(0, len(m), 512):
      chunks.append(m[i:i+512])

    w = []
    for chunk in chunks:
      for i in range(0, 16):
        w.append(chunk[ (i*32) : (i*32)+32 ])
      for i in range(16, 80):
        word_xor = w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16]
        word = ((word_xor << 1) & 0xfffffffe) | ((word_xor >> 31) & 0x00000001)
        w.append(word)

    a = self.h0
    b = self.h1
    c = self.h2
    d = self.h3
    e = self.h4

    for Main_Iteration in range(80):
      if Main_Iteration < 20:
        f = \
        ( \
          (int.from_bytes(b, 'big') & int.from_bytes(c, 'big'))    | \
          (~(int.from_bytes(b, 'big')) & int.from_bytes(d, 'big')) \
        ).to_bytes(4, 'big')
        k = 0x5a827999
      elif Main_Iteration < 40:
        f = (int.from_bytes(b, 'big') ^ int.from_bytes(c, 'big') ^ int.from_bytes(d, 'big')).to_bytes(4, 'big')
        k = 0x6ed9eba1
      elif Main_Iteration < 60:
        f = \
        ( \
          (int.from_bytes(b, 'big') & int.from_bytes(c, 'big')) | \
          (int.from_bytes(b, 'big') & int.from_bytes(d, 'big')) | \
          (int.from_bytes(c, 'big') & int.from_bytes(d, 'big')) \
        ).to_bytes(4, 'big')
        k = 0x8f1bbcdc
      else:
        f = \
        ( \
          int.from_bytes(b, 'big') ^ int.from_bytes(c, 'big') ^ int.from_bytes(d, 'big') \
        ).to_bytes(4, 'big')
        k = 0xca62c1d6

      temp = ((a << 5) & 0xffffffe0 | (a >> 27) & 0x00000005) + f + e + k + w[i]
      e = d
      d = c
      c = (b leftrotate 30)
      b = a
      a = temp

    h0 += a
    h1 += b
    h2 += c
    h3 += d
    h4 += e

#  hh = (h0 leftshift 128) | (h1 leftshift 96) | (h2 leftshift 64) | (h3 leftshift 32) | h4

def main():
  x1 = b'Fox'
  x2 = b'The red fox\njumps over\nthe blue dog'
  x3 = b'The red fox\njumps ouer\nthe blue dog'
  x4 = b'The red fox\njumps oevr\nthe blue dog'
  x5 = b'The red fox\njumps oer\nthe blue dog'

  mysha1 = SHA1_28()

