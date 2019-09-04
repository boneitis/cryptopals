'''
$ python3 s27.py

'''

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto import Random
from Crypto.Util.strxor import strxor

class CBC_Oracle_27:
  def __init__(self):
    self.key = Random.get_random_bytes(16)
    self.bs = 16
    self.iv = self.key
    self.mode = AES.MODE_CBC
    self.invalid_ascii = False

  def sanitize(self, b):
    return b.replace(';', '').replace('=', '')

  def check_valid_ascii(self, m):
    for i in range(127, 256):
      if i in m:
        return False
    return True

  def encryption_circuit(self, b):
    cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
    prefix = b'comment1=cooking%20MCs;userdata='
    postfix = b';comment2=%20like%20a%20pound%20of%20bacon'
    m = prefix + self.sanitize(b).encode() + postfix
    c = cipher.encrypt(pad(prefix+self.sanitize(b).encode()+postfix, self.bs, style = 'pkcs7'))
    return c

  def decrypt_and_check_ascii(self, b):
    try:
      cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
      self.m = cipher.decrypt(b)
      if not self.check_valid_ascii(self.m):
        raise NotValidASCII
      self.invalid_ascii = False
      print('Decrypt OK.\n', self.m, end='\n\n')
    except NotValidASCII:
      self.invalid_ascii = True
      print('Invalid ASCII in decrypted string.')

  def fetch_bad_pt(self):
    if self.invalid_ascii == True:
      print('Fault trip. Returning PT.\n', self.m, end='\n\n')
      return self.m
    else:
      print('Could not trip fault. Withholding PT.')
      return

  def challenge_key(self, k):
#    print('comparing submitted key: ', k, '\nwith oracle\'s key: ', self.key)
    if k == self.key:
      return True
    else:
      return False

class NotValidASCII(Exception):
  pass

def main():
  mal = CBC_Oracle_27()
  c = mal.encryption_circuit('A' * 8)
#  mal.decrypt_and_check_ascii(c)
  c = c[:16] + (b'\x00' * 16) + c[:16] + Random.get_random_bytes(256)
  mal.decrypt_and_check_ascii(c)
  p = mal.fetch_bad_pt()
  if p:
    key = strxor(p[:16], p[32:48])
    if mal.challenge_key(key):
      print('huzzah')
    else:
      print('kaboom')
  else:
    print('Main: kaboom')

if __name__ == '__main__':
  main()

