'''
$ python3 s29.py


'''

from Crypto.Random import get_random_bytes
from Crypto.Random.random import randint
from Crypto.Random.random import choice
from Crypto.Util.strxor import strxor

class SHA1_29:
  def __init__(self):
    self.h0_0 = 0x67452301
    self.h1_0 = 0xefcdab89
    self.h2_0 = 0x98badcfe
    self.h3_0 = 0x10325476
    self.h4_0 = 0xc3d2e1f0
###    self.key = choice(open('/usr/share/dict/words').read().splitlines()).encode()
    self.key = b'AAAA'
    self.known_pt = b'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon'

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

  def digest(self, m, stage=None):
    print('stage:', stage)
    if stage is None:
      h0 = self.h0_0
      h1 = self.h1_0
      h2 = self.h2_0
      h3 = self.h3_0
      h4 = self.h4_0
      m = self.preprocess(m)
    else:
      assert type(stage) is bytes
      assert len(stage) == 20
      # break it up
      stage_register = []
      for i in range(5):
        stage_register.append(int.from_bytes(stage[i*4 : (i+1)*4], 'big'))
#      print(stage_register)
      h0 = stage_register[0]
      h1 = stage_register[1]
      h2 = stage_register[2]
      h3 = stage_register[3]
      h4 = stage_register[4]

#    m = self.preprocess(m)
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

#      if stage is None:
      a = h0
      b = h1
      c = h2
      d = h3
      e = h4
#      else:
#        a = stage_register[0]
#        b = stage_register[1]
#        c = stage_register[2]
#        d = stage_register[3]
#        e = stage_register[4]
#        print(a, b, c, d, e)
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
    return hh

  def challenge(self):
    print('oracle: digesting... ' + (self.key + b'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon').decode() + ' with keylen ' + str(len(self.key)))
    return self.digest(self.key + b'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon')

  def verify(self, m, t):
    return self.digest(m) == t

  def authenticate_admin(self, m, t):
    print('oracle auth: about to digest', self.key, 'and', m)
    if self.digest(self.key + m) == t:
      print('oracle: keylen ' + str(len(self.key)))
      return b';admin=true' in m
    else:
      print('oracle: auth failed, got:\n', self.digest(self.key + m), 'versus\n', t)
      return False

def main():
  x1 = b'Fox'                                          # dfcd3454bbea788a751a696c24d97009ca992d17
  x2 = b'The red fox\njumps over\nthe blue dog'        # 008646bbfb7dcbe2823cacc76cd190b1ee6e3abc
  x3 = b'The red fox\njumps ouer\nthe blue dog'        # 8fd8755878514f32d1c676b179a90da4aefe4819
  x4 = b'The red fox\njumps oevr\nthe blue dog'        # fcd37fdb5af2c6ff915fd401c0a97d9a46affb45
  x5 = b'The red fox\njumps oer\nthe blue dog'         # 8acad682d5884c754bf417997d88bcf892b96a6c

  mysha1 = SHA1_29()
#  tag = mysha1.digest(x1)
#  print(tag.hex())

#  if mysha1.verify(x1, tag):
#    print('huzzah')
#  else:
#    print('kaboom')

  challenge = mysha1.challenge()

  aux = SHA1_29()

  original_message = b'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon'
#  new_message = b';admin=true' + b'\x80' + (b'\x00' * 44) + (1112).to_bytes(8, 'big')
  new_message = b';admin=true'

  resume_tag = aux.digest(new_message + b'\x80' + (b'\x00' * 44) + (1112).to_bytes(8, 'big'), challenge)
  print('resume:\n', resume_tag)

#  for guess_keylen in range(1, 24):
  for guess_keylen in range(4,5):
    glue_padding = b'\x80' + ((120 - (77 + guess_keylen + 1)) * b'\x00') + ((77 + guess_keylen)*8).to_bytes(8, 'big')
    query = original_message + glue_padding + new_message
    if mysha1.authenticate_admin(query, resume_tag):
      print('authenticated at keylen ' + str(guess_keylen))
      print('huzzah')
      break
    else:
      print(str(guess_keylen) + '...kaboom')

#  tag = mysha1.challenge(x2)
#  print(tag.hex())

#  tag = mysha1.challenge(x3)
#  print(tag.hex())

#  tag = mysha1.challenge(x4)
#  print(tag.hex())

#  tag = mysha1.challenge(x5)
#  print(tag.hex())

if __name__ == '__main__':
  main()

