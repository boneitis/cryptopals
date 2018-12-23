'''
s16.py

'''

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class CBC_Oracle_16:
  def __init__(self, KEY=b'YELLOW SUBMARINE', MODE=2, IV=b'\x00'*16):
#    from Crypto.Cipher import AES
#    from Crypto.Util.Padding import pad
    self.key = KEY
    self.mode = MODE
    self.iv = IV
    self.c = AES.new(self.key, self.mode, self.iv)
    self.bs = 16

  def sanitize(self, b):
    return b.replace('&', '').replace('=', '')

  def o_encrypt(self, b):
    prefix = b'comment1=cooking%20MCs;userdata='
    postfix = b';comment2=%20like%20a%20pound%20of%20bacon'
    print('encrypting:')
    print(pad(prefix+self.sanitize(b).encode()+postfix, self.bs, style='pkcs7'))
    return self.c.encrypt(pad(prefix+self.sanitize(b).encode()+postfix, self.bs, style='pkcs7'))

def main():
  mary = CBC_Oracle_16()
  mary.o_encrypt('hiaefeaaaaaauseraadmin')

if __name__=='__main__':
  main()

