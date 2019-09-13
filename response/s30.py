'''
$ python3 s30.py


print(hashlib.new("md4", b'asdf'.hexdigest())

'''
from Crypto.Random.random import choice

class MD4_30:
  def __init__(self):
    self.A_0 = 0x67452301
    self.B_0 = 0xefcdab89
    self.C_0 = 0x98badcfe
    self.D_0 = 0x10325476
    self.Magic2 = 0x5a827999
    self.Magic3 = 0x6ed9eba1
#    self.key = b'AAAA'
    self.key = choice(open('/usr/share/dict/words').read().splitlines()).encode()

  def preprocess(self, m):
    ml = len(m) * 8
    m += b'\x80'
    padding = 448 - ((ml + 8) % 512)
    if padding < 0:
      padding += 512
    assert padding % 8 == 0
    padding_bytes_len = int(padding / 8)
    m += (b'\x00' * padding_bytes_len) + ml.to_bytes(8, 'little')
    return m

  def f(self, X, Y, Z):
    return (X & Y) | (((~X) & 0xffffffff) & Z)

  def g(self, X, Y, Z):
    return (X & Y) | (X & Z) | (Y & Z)

  def h(self, X, Y, Z):
    return X ^ Y ^ Z

  # A = (A + f(B,C,D) + X[i]) << s
  def round1(self, A, B, C, D, X):
    A = (A + self.f(B, C, D) + X[0]) % 0x100000000
    A = ((A << 3) & 0xfffffff8) | ((A >> 29) & 0x00000007)
    D = (D + self.f(A, B, C) + X[1]) % 0x100000000
    D = ((D << 7) & 0xffffff80) | ((D >> 25) & 0x0000007f)
    C = (C + self.f(D, A, B) + X[2]) % 0x100000000
    C = ((C << 11) & 0xfffff800) | ((C >> 21) & 0x000007ff)
    B = (B + self.f(C, D, A) + X[3]) % 0x100000000
    B = ((B << 19) & 0xfff80000) | ((B >> 13) & 0x0007ffff)

    A = (A + self.f(B, C, D) + X[4]) % 0x100000000
    A = ((A << 3) & 0xfffffff8) | ((A >> 29) & 0x00000007)
    D = (D + self.f(A, B, C) + X[5]) % 0x100000000
    D = ((D << 7) & 0xffffff80) | ((D >> 25) & 0x0000007f)
    C = (C + self.f(D, A, B) + X[6]) % 0x100000000
    C = ((C << 11) & 0xfffff800) | ((C >> 21) & 0x000007ff)
    B = (B + self.f(C, D, A) + X[7]) % 0x100000000
    B = ((B << 19) & 0xfff80000) | ((B >> 13) & 0x0007ffff)

    A = (A + self.f(B, C, D) + X[8]) % 0x100000000
    A = ((A << 3) & 0xfffffff8) | ((A >> 29) & 0x00000007)
    D = (D + self.f(A, B, C) + X[9]) % 0x100000000
    D = ((D << 7) & 0xffffff80) | ((D >> 25) & 0x0000007f)
    C = (C + self.f(D, A, B) + X[10]) % 0x100000000
    C = ((C << 11) & 0xfffff800) | ((C >> 21) & 0x000007ff)
    B = (B + self.f(C, D, A) + X[11]) % 0x100000000
    B = ((B << 19) & 0xfff80000) | ((B >> 13) & 0x0007ffff)

    A = (A + self.f(B, C, D) + X[12]) % 0x100000000
    A = ((A << 3) & 0xfffffff8) | ((A >> 29) & 0x00000007)
    D = (D + self.f(A, B, C) + X[13]) % 0x100000000
    D = ((D << 7) & 0xffffff80) | ((D >> 25) & 0x0000007f)
    C = (C + self.f(D, A, B) + X[14]) % 0x100000000
    C = ((C << 11) & 0xfffff800) | ((C >> 21) & 0x000007ff)
    B = (B + self.f(C, D, A) + X[15]) % 0x100000000
    B = ((B << 19) & 0xfff80000) | ((B >> 13) & 0x0007ffff)

    return [A, B, C, D]

  # A = (A + g(B,C,D) + X[i] + self.Magic2) << s
  def round2(self, A, B, C, D, X):
    A = (A + self.g(B, C, D) + X[0] + self.Magic2) % 0x100000000
    A = ((A << 3) & 0xfffffff8) | ((A >> 29) & 0x00000007)
    D = (D + self.g(A, B, C) + X[4] + self.Magic2) % 0x100000000
    D = ((D << 5) & 0xffffffe0) | ((D >> 27) & 0x0000001f)
    C = (C + self.g(D, A, B) + X[8] + self.Magic2) % 0x100000000
    C = ((C << 9) & 0xfffffe00) | ((C >> 23) & 0x000001ff)
    B = (B + self.g(C, D, A) + X[12] + self.Magic2) % 0x100000000
    B = ((B << 13) & 0xffffe000) | ((B >> 19) & 0x00001fff)

    A = (A + self.g(B, C, D) + X[1] + self.Magic2) % 0x100000000
    A = ((A << 3) & 0xfffffff8) | ((A >> 29) & 0x00000007)
    D = (D + self.g(A, B, C) + X[5] + self.Magic2) % 0x100000000
    D = ((D << 5) & 0xffffffe0) | ((D >> 27) & 0x0000001f)
    C = (C + self.g(D, A, B) + X[9] + self.Magic2) % 0x100000000
    C = ((C << 9) & 0xfffffe00) | ((C >> 23) & 0x000001ff)
    B = (B + self.g(C, D, A) + X[13] + self.Magic2) % 0x100000000
    B = ((B << 13) & 0xffffe000) | ((B >> 19) & 0x00001fff)

    A = (A + self.g(B, C, D) + X[2] + self.Magic2) % 0x100000000
    A = ((A << 3) & 0xfffffff8) | ((A >> 29) & 0x00000007)
    D = (D + self.g(A, B, C) + X[6] + self.Magic2) % 0x100000000
    D = ((D << 5) & 0xffffffe0) | ((D >> 27) & 0x0000001f)
    C = (C + self.g(D, A, B) + X[10] + self.Magic2) % 0x100000000
    C = ((C << 9) & 0xfffffe00) | ((C >> 23) & 0x000001ff)
    B = (B + self.g(C, D, A) + X[14] + self.Magic2) % 0x100000000
    B = ((B << 13) & 0xffffe000) | ((B >> 19) & 0x00001fff)

    A = (A + self.g(B, C, D) + X[3] + self.Magic2) % 0x100000000
    A = ((A << 3) & 0xfffffff8) | ((A >> 29) & 0x00000007)
    D = (D + self.g(A, B, C) + X[7] + self.Magic2) % 0x100000000
    D = ((D << 5) & 0xffffffe0) | ((D >> 27) & 0x0000001f)
    C = (C + self.g(D, A, B) + X[11] + self.Magic2) % 0x100000000
    C = ((C << 9) & 0xfffffe00) | ((C >> 23) & 0x000001ff)
    B = (B + self.g(C, D, A) + X[15] + self.Magic2) % 0x100000000
    B = ((B << 13) & 0xffffe000) | ((B >> 19) & 0x00001fff)

    return [A, B, C, D]
  
  # A = (A + h(B,C,D) + X[i] + self.Magic3) << s
  def round3(self, A, B, C, D, X):
    A = (A + self.h(B, C, D) + X[0] + self.Magic3) % 0x100000000
    A = ((A << 3) & 0xfffffff8) | ((A >> 29) & 0x00000007)
    D = (D + self.h(A, B, C) + X[8] + self.Magic3) % 0x100000000
    D = ((D << 9) & 0xfffffe00) | ((D >> 23) & 0x000001ff)
    C = (C + self.h(D, A, B) + X[4] + self.Magic3) % 0x100000000
    C = ((C << 11) & 0xfffff800) | ((C >> 21) & 0x000007ff)
    B = (B + self.h(C, D, A) + X[12] + self.Magic3) % 0x100000000
    B = ((B << 15) & 0xffffe000) | ((B >> 17) & 0x0001ffff)

    A = (A + self.h(B, C, D) + X[2] + self.Magic3) % 0x100000000
    A = ((A << 3) & 0xfffffff8) | ((A >> 29) & 0x00000007)
    D = (D + self.h(A, B, C) + X[10] + self.Magic3) % 0x100000000
    D = ((D << 9) & 0xfffffe00) | ((D >> 23) & 0x000001ff)
    C = (C + self.h(D, A, B) + X[6] + self.Magic3) % 0x100000000
    C = ((C << 11) & 0xfffff800) | ((C >> 21) & 0x000007ff)
    B = (B + self.h(C, D, A) + X[14] + self.Magic3) % 0x100000000
    B = ((B << 15) & 0xffffe000) | ((B >> 17) & 0x0001ffff)

    A = (A + self.h(B, C, D) + X[1] + self.Magic3) % 0x100000000
    A = ((A << 3) & 0xfffffff8) | ((A >> 29) & 0x00000007)
    D = (D + self.h(A, B, C) + X[9] + self.Magic3) % 0x100000000
    D = ((D << 9) & 0xfffffe00) | ((D >> 23) & 0x000001ff)
    C = (C + self.h(D, A, B) + X[5] + self.Magic3) % 0x100000000
    C = ((C << 11) & 0xfffff800) | ((C >> 21) & 0x000007ff)
    B = (B + self.h(C, D, A) + X[13] + self.Magic3) % 0x100000000
    B = ((B << 15) & 0xffffe000) | ((B >> 17) & 0x0001ffff)

    A = (A + self.h(B, C, D) + X[3] + self.Magic3) % 0x100000000
    A = ((A << 3) & 0xfffffff8) | ((A >> 29) & 0x00000007)
    D = (D + self.h(A, B, C) + X[11] + self.Magic3) % 0x100000000
    D = ((D << 9) & 0xfffffe00) | ((D >> 23) & 0x000001ff)
    C = (C + self.h(D, A, B) + X[7] + self.Magic3) % 0x100000000
    C = ((C << 11) & 0xfffff800) | ((C >> 21) & 0x000007ff)
    B = (B + self.h(C, D, A) + X[15] + self.Magic3) % 0x100000000
    B = ((B << 15) & 0xffffe000) | ((B >> 17) & 0x0001ffff)

    return [A, B, C, D]

  def digest(self, m, stage = None):
    if stage is None:
      print('stage none')
      A = self.A_0
      B = self.B_0
      C = self.C_0
      D = self.D_0
      m = self.preprocess(m)
#      print('m pre-processed:', m)
    else:
      assert type(stage) is bytes
      assert len(stage) == 16
      stage_register = []
      for i in range(4):
        stage_register.append(int.from_bytes(stage[i*4 : (i+1)*4], 'little'))
      A = stage_register[0]
      B = stage_register[1]
      C = stage_register[2]
      D = stage_register[3]

    chunks = []
    for i in range(0, len(m), 64):
      chunks.append(m[i : i + 64])

    for chunk in chunks:
      AA = A
      BB = B
      CC = C
      DD = D
      X = []
      for j in range(16):
#        temp = chunk[(j*4):(j*4)+4]
#        print('temp:', temp)
#        X.append(int.from_bytes(temp[2:] + temp[:2], 'little'))
        X.append(int.from_bytes(chunk[(j * 4) : (j*4)+4 ], 'little'))
##      print('chunk:', chunk)
##      print('X:', X, end='\n\n')
##      print('Before Anything:\nA:', A, 'B:', B, 'C:', C, 'D:', D)

      ABCD = self.round1(A, B, C, D, X)
##      print('Round 1 results:\nA:', ABCD[0], 'B:', ABCD[1], 'C:', ABCD[2], 'D:', ABCD[3])
      ABCD = self.round2(ABCD[0], ABCD[1], ABCD[2], ABCD[3], X)
##      print('Round 2 results:\nA:', ABCD[0], 'B:', ABCD[1], 'C:', ABCD[2], 'D:', ABCD[3])
      ABCD = self.round3(ABCD[0], ABCD[1], ABCD[2], ABCD[3], X)
##      print('Round 3 results:\nA:', ABCD[0], 'B:', ABCD[1], 'C:', ABCD[2], 'D:', ABCD[3])

      A = (ABCD[0] + AA) % 0x100000000
##     print('Round 3 results:\nA:', A, 'B:', B, 'C:', C, 'D:', D)
      B = (ABCD[1] + BB) % 0x100000000
      C = (ABCD[2] + CC) % 0x100000000
      D = (ABCD[3] + DD) % 0x100000000

    a = A.to_bytes(4, 'little')
    b = B.to_bytes(4, 'little')
    c = C.to_bytes(4, 'little')
    d = D.to_bytes(4, 'little')
    return a + b + c + d

  def challenge(self):
    print('oracle: digesting... ' + (self.key + b'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon').decode() + ' with keylen ' + str(len(self.key)))
    return self.digest(self.key + b'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon')

  def verify(self, m, t):
    return self.digest(m) == t

  def authenticate_admin(self, m, t):
    if self.digest(self.key + m) == t:
      return b';admin=true' in m
    else:
      return False


def main():
#  x1 = b''                                             # 31d6cfe0d16ae931b73c59d7e0c089c0
#  x2 = b'a'                                            # bde52cb31de33e46245e05fbdbd6fb24
#  x3 = b'abc'                                          # a448017aaf21d8525fc10ae87aa6729d
#  x4 = b'message digest'                               # d9130a8164549fe818874806e1c7014b
#  x5 = b'abcdefghijklmnopqrstuvwxyz'                   # d79e1c308aa5bbcdeea8ed63df412da9
#  x6 = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'                    # 043f8582f241db351ce627e153e7f0e4
#  x7 = b'12345678901234567890123456789012345678901234567890123456789012345678901234567890'  # e33b4ddc9c38f2199c3e7b164fcc0536
#  x8 = b'The quick brown fox jumps over the lazy dog'  # 1bee69a46ba811185c194762abaeae90
#  x9 = b'The quick brown fox jumps over the lazy cog'  # b86e130ce7028da59e672d56ad0113df

  md4 = MD4_30()
#  print(md4.digest(x1).hex())
#  print(md4.digest(x2).hex())
#  print(md4.digest(x3).hex())
#  print(md4.digest(x4).hex())
#  print(md4.digest(x5).hex())
#  print(md4.digest(x6).hex())
#  print(md4.digest(x7).hex())

  challenge = md4.challenge()

  aux = MD4_30()

  original_message = b'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon'
  new_message = b';admin=true'

  resume_tag = aux.digest(new_message + b'\x80' + (b'\x00' * 44) + (1112).to_bytes(8, 'little'), challenge)
  for guess_keylen in range(1, 24):
    glue_padding = b'\x80' + ((120 - (77 + guess_keylen + 1)) * b'\x00') + ((77 + guess_keylen)*8).to_bytes(8, 'little')
    query = original_message + glue_padding + new_message
    if md4.authenticate_admin(query, resume_tag):
      print('authenticated at keylen ' + str(guess_keylen))
      print('huzzah')
      break
    else:
      print(str(guess_keylen) + '...kaboom')

if __name__ == '__main__':
  main()
