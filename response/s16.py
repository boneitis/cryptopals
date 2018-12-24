'''
$ python3 s16.py

'''

import sys
import random as r
r.seed()
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class CBC_Oracle_16:
  def __init__(self, KEY=bytes([r.randint(0,255) for x in range(16)]), MODE=2, IV=b'\x00'*16):
    self.key = KEY
    self.mode = MODE
    self.iv = IV
    self.c = AES.new(self.key, self.mode, self.iv)
    self.p = AES.new(self.key, self.mode, self.iv)
    self.bs = 16

  def sanitize(self, b):
    return b.replace(';', '').replace('=', '')

  def encryption_circuit(self, b):
    prefix = b'comment1=cooking%20MCs;userdata='
    postfix = b';comment2=%20like%20a%20pound%20of%20bacon'
    print('pt before encrypting:')
    print(pad(prefix+self.sanitize(b).encode()+postfix, self.bs, style='pkcs7'))
    return self.c.encrypt(pad(prefix+self.sanitize(b).encode()+postfix, self.bs, style='pkcs7'))

  def decrypt_and_check_admin(self, b):
    print('\npt after decrypting:')
    o = unpad(self.p.decrypt(b), self.bs, style='pkcs7')
    print(o)
    if o.find(b';admin=true;') >= 0:
      return True
    else:
      return False

# semicolon ';':   \x3b
# equal sign '=':  \x3d
def main():
  mary = CBC_Oracle_16()
  c = mary.encryption_circuit('aaaaaKadminMtrue')
  c_nefarious = c[:21] + int.to_bytes(c[21]^112, 1, byteorder=sys.byteorder) + c[22:27] + int.to_bytes(c[27]^112, 1, byteorder=sys.byteorder) + c[28:]
  if(mary.decrypt_and_check_admin(c_nefarious)):
    print('\nhuzzah')
  else:
    print('\nblast!')

if __name__ == '__main__':
  main()

