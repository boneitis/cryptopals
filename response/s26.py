'''
$ python3 s26.py

'''

from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random
from Crypto.Util.strxor import strxor

class CTR_Oracle_26:
  def __init__(self):
    self.nonce = (0).to_bytes(8, 'little')
    self.ctr = Counter.new(64, prefix = self.nonce, little_endian = True, initial_value = 0)
    self.key = Random.get_random_bytes(16)
    self.cipher = AES.new(self.key, AES.MODE_CTR, counter = self.ctr)

  def sanitize(self, b):
    return b.replace(';', '').replace('=', '')

  def encryption_circuit(self, b):
    prefix = b'comment1=cooking%20MCs;userdata='
    postfix = b';comment2=%20like%20a%20pound%20of%20bacon'
    pt = prefix + self.sanitize(b).encode() + postfix
    print('pt before encrypting:')
    print(pt)
    return self.cipher.encrypt(pt)

  def decrypt_and_check_admin(self, b):
    self.ctr = Counter.new(64, prefix = self.nonce, little_endian = True, initial_value = 0)
    self.cipher = AES.new(self.key, AES.MODE_CTR, counter = self.ctr)
    o = self.cipher.decrypt(b)
    print('\npt after decrypting:')
    print(o)
    if o.find(b';admin=true;') >= 0:
      return True
    else:
      return False

def main():
  maria = CTR_Oracle_26()
  c = maria.encryption_circuit('aAadminAtrue')
  c_nefarious = c[:33] + (c[33] ^ 65 ^ 59).to_bytes(1, 'little') + c[34:39] + (c[39] ^ 65 ^ 61).to_bytes(1, 'little') + c[40:]
  if maria.decrypt_and_check_admin(c_nefarious):
    print('huzzah')
  else:
    print('kaboom')

if __name__ == '__main__':
  main()

