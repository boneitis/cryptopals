'''
$ python3 s25.py

'''
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.Padding import unpad
from Crypto import Random
from Crypto.Util.strxor import strxor

class Oracle25:
  def __init__(self):
    self.pt = self.fetch_pt()
    self.nonce = (0).to_bytes(8, 'little')
    self.ctr = Counter.new(64, prefix = self.nonce, little_endian = True, initial_value = 0)
    self.key = Random.get_random_bytes(16)
    self.cipher = AES.new(self.key, AES.MODE_CTR, counter = self.ctr)
    self.ct = self.cipher.encrypt(self.pt)

  def fetch_pt(self):
    cipher = AES.new(b'YELLOW SUBMARINE', AES.MODE_ECB)
    with open('challenge/25.txt', 'r') as f:
      data = f.read().replace('\n', '')
    return unpad(cipher.decrypt(b64decode(data)), 16)

  def challenge(self):
    return self.ct

  def edit(self, ct, key, offset, newtext):
    assert(offset < len(ct))
    assert(type(newtext) is bytes)
    assert(len(newtext) == 1)
    self.ctr = Counter.new(64, prefix = self.nonce, little_endian = True, initial_value = 0)
    self.cipher = AES.new(self.key, AES.MODE_CTR, counter = self.ctr)
    pt = self.cipher.decrypt(ct)
    keystream = strxor(pt, ct)
    return strxor(newtext, keystream[offset].to_bytes(1, 'little'))

  def edit_pub(self, ct, offset, newtext):
    return self.edit(ct, self.key, offset, newtext)

def main():
  o25 = Oracle25()
  challenge = o25.challenge()

  ct_prime = b''
  for i in range(len(challenge)):
    ct_prime += o25.edit_pub(challenge, i, b'A')

  leaked_keystream = strxor(ct_prime, b'A' * len(challenge))
  response = strxor(leaked_keystream, challenge)
  print(response.decode())

if __name__ == '__main__':
  main()

