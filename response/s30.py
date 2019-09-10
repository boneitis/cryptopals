'''
$ python3 s30.py


print(hashlib.new("md4", b'asdf'.hexdigest())

'''
import hashlib

class MD4_30:
  def __init__(self):
    self.A_0 = 0x67452301
    self.B_0 = 0xefcdab89
    self.C_0 = 0x98badcfe
    self.D_0 = 0x10325476
#    self.A_0 = 0x01234567
#    self.B_0 = 0x89abcdef
#    self.C_0 = 0xfedcba98
#    self.D_0 = 0x76543210
    self.Magic2 = 0x5a827999
    self.Magic3 = 0x6ed9eba1
    self.Mask = 0xffffffff

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
    A = (A << 3) & self.Mask
    D = (D + self.f(A, B, C) + X[1]) % 0x100000000
    D = (D << 7) & self.Mask
    C = (C + self.f(D, A, B) + X[2]) % 0x100000000
    C = (C << 11) & self.Mask
    B = (B + self.f(C, D, A) + X[3]) % 0x100000000
    B = (B << 19) & self.Mask

    A = (A + self.f(B, C, D) + X[4]) % 0x100000000
    A = (A << 3) & self.Mask
    D = (D + self.f(A, B, C) + X[5]) % 0x100000000
    D = (D << 7) & self.Mask
    C = (C + self.f(D, A, B) + X[6]) % 0x100000000
    C = (C << 11) & self.Mask
    B = (B + self.f(C, D, A) + X[7]) % 0x100000000
    B = (B << 19) & self.Mask

    A = (A + self.f(B, C, D) + X[8]) % 0x100000000
    A = (A << 3) & self.Mask
    D = (D + self.f(A, B, C) + X[9]) % 0x100000000
    D = (D << 7) & self.Mask
    C = (C + self.f(D, A, B) + X[10]) % 0x100000000
    C = (C << 11) & self.Mask
    B = (B + self.f(C, D, A) + X[11]) % 0x100000000
    B = (B << 19) & self.Mask

    A = (A + self.f(B, C, D) + X[12]) % 0x100000000
    A = (A << 3) & self.Mask
    D = (D + self.f(A, B, C) + X[13]) % 0x100000000
    D = (D << 7) & self.Mask
    C = (C + self.f(D, A, B) + X[14]) % 0x100000000
    C = (C << 11) & self.Mask
    B = (B + self.f(C, D, A) + X[15]) % 0x100000000
    B = (B << 19) & self.Mask

    return [A, B, C, D]

  # A = (A + g(B,C,D) + X[i] + self.Magic2) << s
  def round2(self, A, B, C, D, X):
    A = (A + self.g(B, C, D) + X[0] + self.Magic2) % 0x100000000
    A = (A << 3) & self.Mask
    D = (D + self.g(A, B, C) + X[4] + self.Magic2) % 0x100000000
    D = (D << 5) & self.Mask
    C = (C + self.g(D, A, B) + X[8] + self.Magic2) % 0x100000000
    C = (C << 9) & self.Mask
    B = (B + self.g(C, D, A) + X[12] + self.Magic2) % 0x100000000
    B = (B << 13) & self.Mask

    A = (A + self.g(B, C, D) + X[1] + self.Magic2) % 0x100000000
    A = (A << 3) & self.Mask
    D = (D + self.g(A, B, C) + X[5] + self.Magic2) % 0x100000000
    D = (D << 5) & self.Mask
    C = (C + self.g(D, A, B) + X[9] + self.Magic2) % 0x100000000
    C = (C << 9) & self.Mask
    B = (B + self.g(C, D, A) + X[13] + self.Magic2) % 0x100000000
    B = (B << 13) & self.Mask

    A = (A + self.g(B, C, D) + X[2] + self.Magic2) % 0x100000000
    A = (A << 3) & self.Mask
    D = (D + self.g(A, B, C) + X[6] + self.Magic2) % 0x100000000
    D = (D << 5) & self.Mask
    C = (C + self.g(D, A, B) + X[10] + self.Magic2) % 0x100000000
    C = (C << 9) & self.Mask
    B = (B + self.g(C, D, A) + X[14] + self.Magic2) % 0x100000000
    B = (B << 13) & self.Mask

    A = (A + self.g(B, C, D) + X[3] + self.Magic2) % 0x100000000
    A = (A << 3) & self.Mask
    D = (D + self.g(A, B, C) + X[7] + self.Magic2) % 0x100000000
    D = (D << 5) & self.Mask
    C = (C + self.g(D, A, B) + X[11] + self.Magic2) % 0x100000000
    C = (C << 9) & self.Mask
    B = (B + self.g(C, D, A) + X[15] + self.Magic2) % 0x100000000
    B = (B << 13) & self.Mask

    return [A, B, C, D]
  
  # A = (A + h(B,C,D) + X[i] + self.Magic3) << s
  def round3(self, A, B, C, D, X):
    A = (A + self.h(B, C, D) + X[0] + self.Magic3) % 0x100000000
    A = (A << 3) & self.Mask
    D = (D + self.h(A, B, C) + X[8] + self.Magic3) % 0x100000000
    D = (D << 9) & self.Mask
    C = (C + self.h(D, A, B) + X[4] + self.Magic3) % 0x100000000
    C = (C << 11) & self.Mask
    B = (B + self.h(C, D, A) + X[12] + self.Magic3) % 0x100000000
    B = (B << 15) & self.Mask

    A = (A + self.h(B, C, D) + X[2] + self.Magic3) % 0x100000000
    A = (A << 3) & self.Mask
    D = (D + self.h(A, B, C) + X[10] + self.Magic3) % 0x100000000
    D = (D << 9) & self.Mask
    C = (C + self.h(D, A, B) + X[6] + self.Magic3) % 0x100000000
    C = (C << 11) & self.Mask
    B = (B + self.h(C, D, A) + X[14] + self.Magic3) % 0x100000000
    B = (B << 15) & self.Mask

    A = (A + self.h(B, C, D) + X[1] + self.Magic3) % 0x100000000
    A = (A << 3) & self.Mask
    D = (D + self.h(A, B, C) + X[9] + self.Magic3) % 0x100000000
    D = (D << 9) & self.Mask
    C = (C + self.h(D, A, B) + X[5] + self.Magic3) % 0x100000000
    C = (C << 11) & self.Mask
    B = (B + self.h(C, D, A) + X[13] + self.Magic3) % 0x100000000
    B = (B << 15) & self.Mask

    A = (A + self.h(B, C, D) + X[3] + self.Magic3) % 0x100000000
    A = (A << 3) & self.Mask
    D = (D + self.h(A, B, C) + X[11] + self.Magic3) % 0x100000000
    D = (D << 9) & self.Mask
    C = (C + self.h(D, A, B) + X[7] + self.Magic3) % 0x100000000
    C = (C << 11) & self.Mask
    B = (B + self.h(C, D, A) + X[15] + self.Magic3) % 0x100000000
    B = (B << 15) & self.Mask

    return [A, B, C, D]

  def digest(self, m, stage = None):
    if stage is None:
      print('stage none')
      A = self.A_0
      B = self.B_0
      C = self.C_0
      D = self.D_0
#      AA = A
#      BB = B
#      CC = C
#      DD = D
      m = self.preprocess(m)
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
#      AA = A
#      BB = B
#      CC = C
#      DD = D

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
      print('chunk:', chunk)
      print('X:', X, end='\n\n')

      ABCD = self.round1(A, B, C, D, X)
      ABCD = self.round2(ABCD[0], ABCD[1], ABCD[2], ABCD[3], X)
      ABCD = self.round3(ABCD[0], ABCD[1], ABCD[2], ABCD[3], X)

      A = (ABCD[0] + AA) % 0x100000000
      B = (ABCD[1] + BB) % 0x100000000
      C = (ABCD[2] + CC) % 0x100000000
      D = (ABCD[3] + DD) % 0x100000000

    a = A.to_bytes(4, 'little')
    b = B.to_bytes(4, 'little')
    c = C.to_bytes(4, 'little')
    d = D.to_bytes(4, 'little')
    return a + b + c + d

def main():
  x1 = b''                                             # 31d6cfe0d16ae931b73c59d7e0c089c0
  x2 = b'a'                                            # bde52cb31de33e46245e05fbdbd6fb24
  x3 = b'abc'                                          # a448017aaf21d8525fc10ae87aa6729d
  x4 = b'message digest'                               # d9130a8164549fe818874806e1c7014b
  x5 = b'abcdefghijklmnopqrstuvwxyz'                   # d79e1c308aa5bbcdeea8ed63df412da9
  x6 = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'                    # 043f8582f241db351ce627e153e7f0e4
  x7 = b'12345678901234567890123456789012345678901234567890123456789012345678901234567890'  # e33b4ddc9c38f2199c3e7b164fcc0536
  x8 = b'The quick brown fox jumps over the lazy dog'  # 1bee69a46ba811185c194762abaeae90
  x9 = b'The quick brown fox jumps over the lazy cog'  # b86e130ce7028da59e672d56ad0113df

  md4 = MD4_30()
#  ret = md4.digest(b'A' * 32 + b'B' * 64 + b'C' * 64 + b'D')
  ret = md4.digest(x3)
  print(ret.hex())

if __name__ == '__main__':
  main()
