'''
$ python3 s28.py


'''

import sys
from Crypto.Util.strxor import strxor

class SHA1_28:
  def __init__(self):
    self.h0_0 = 0x67452301
    self.h1_0 = 0xefcdab89
    self.h2_0 = 0x98badcfe
    self.h3_0 = 0x10325476
    self.h4_0 = 0xc3d2e1f0

  def preprocess(self, m):
    ml = len(m) * 8
    m += b'\x80'
    padding = 448 - ((ml+8)%512)
    if padding < 0:
      padding += 512
    assert(padding % 8 == 0)
    padding_bytes_len = int(padding/8)
    m += (b'\x00' * padding_bytes_len) + ml.to_bytes(8, 'big')
#    print('post-pre-process length', len(m), 'of m: \n', m)
    return m

  def digest(self, m):
    h0 = self.h0_0
    h1 = self.h1_0
    h2 = self.h2_0
    h3 = self.h3_0
    h4 = self.h4_0

    m = self.preprocess(m)
    chunks = []
    for i in range(0, len(m), 64):
      chunks.append(m[i:i+64])
#    print('number of chunks:', len(chunks))

#    print('len ', len(chunks), 'of chunks:', chunks, end='\n\n\n')

    for chunk in chunks:
      w = []
      for i in range(0, 16):
#        print('appending:',chunk[ (i*4) : (i*4)+4 ])
        w.append(int.from_bytes(chunk[ (i*4) : (i*4)+4 ], 'big'))
#      print('post 16:', w)
      for i in range(16, 80):
        word_xor = w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16]
        word = ((word_xor << 1) & 0xfffffffe) | ((word_xor >> 31) & 0x00000001)
        w.append(word)
#      print('post 80:', w)
#      print('number of words in chunk:', len(w))

      a = h0
      b = h1
      c = h2
      d = h3
      e = h4

      for Main_Iteration in range(80):
        if Main_Iteration < 20:
          f = (b & c) | ((~b) & d)
          k = 0x5a827999
        elif Main_Iteration < 40:
          f = b ^ c ^ d
          k = 0x6ed9eba1
        elif Main_Iteration < 60:
          f = (b & c) | (b & d) | (c & d)
          k = 0x8f1bbcdc
        else:
          f = b ^ c ^ d
          k = 0xca62c1d6

        temp = (((a << 5) & 0xffffffe0 | (a >> 27) & 0x0000001f) + f + e + k + w[Main_Iteration]) % 0x100000000
        e = d
        d = c
        b_lr30 = ((b << 30) & 0xc0000000) | ((b >> 2) & 0x3fffffff)
        c = (b_lr30)
        b = a
        a = temp

      h0 = (h0 + a) % 0x100000000
      h1 = (h1 + b) % 0x100000000
      h2 = (h2 + c) % 0x100000000
      h3 = (h3 + d) % 0x100000000
      h4 = (h4 + e) % 0x100000000

    h0_1 = h0.to_bytes(4, 'big')
    h1_1 = h1.to_bytes(4, 'big')
    h2_1 = h2.to_bytes(4, 'big')
    h3_1 = h3.to_bytes(4, 'big')
    h4_1 = h4.to_bytes(4, 'big')
    hh = h0_1 + h1_1 + h2_1 + h3_1 + h4_1
    print(hh.hex())

def main():
  x1 = b'Fox'                                          # dfcd3454bbea788a751a696c24d97009ca992d17
  x2 = b'The red fox\njumps over\nthe blue dog'        # 008646bbfb7dcbe2823cacc76cd190b1ee6e3abc
  x3 = b'The red fox\njumps ouer\nthe blue dog'        # 8fd8755878514f32d1c676b179a90da4aefe4819
  x4 = b'The red fox\njumps oevr\nthe blue dog'        # fcd37fdb5af2c6ff915fd401c0a97d9a46affb45
  x5 = b'The red fox\njumps oer\nthe blue dog'         # 8acad682d5884c754bf417997d88bcf892b96a6c

  mysha1 = SHA1_28()
#  mysha1.digest(b'A'*64 + b'B'*64 + b'C'*55)
  mysha1.digest(x1)
  mysha1.digest(x2)
  mysha1.digest(x3)
  mysha1.digest(x4)
  mysha1.digest(x5)
  mysha1.digest(b'A'*512 + b'B'*512 + b'C'*512)

if __name__ == '__main__':
  main()

