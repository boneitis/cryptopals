'''
$ python3 s18.py


Problem Description Tolerances
  CTR-128 implementation need only accommodate specifically:
    * 8-byte little endian nonce
    * 8-byte little endian counter

'''

import base64
from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor


class CTR_Iterator():
  def __init__(self, ctr0=2):
    self.maximum = 2 ** (64)
    assert(ctr0 in range(self.maximum))
    self.limit = self.maximum
    self.ctr = ctr0
    self.count = 0
  def __iter__(self):
    return self
  def __next__(self):
    if self.count == self.maximum:
      raise StopIteration
    self.ctr = (self.ctr+1) % self.maximum
    self.count += 1
    return ((self.ctr-1) % self.maximum).to_bytes(8, 'little')

class Nonce_CTR_18():
  def __init__(self, key=b'YELLOW SUBMARINE', nonce=0, ctr0=0):
    self.key = key
    assert(len(self.key) == 16)
    self.half_block_max = 2 ** 64
    assert(                                    \
      nonce in range(self.half_block_max) and  \
      ctr0 in range(self.half_block_max)
    )
    self.nonce = (nonce).to_bytes(8, 'little')
    self.running_ctr = CTR_Iterator(ctr0)
    self.cipher = AES.new(self.key, AES.MODE_ECB)
    self.keystream_buffer = b''

  def generate_keystream(self, requested_length):
    while len(self.keystream_buffer) < requested_length:
      self.keystream_buffer += self.cipher.encrypt(self.nonce + self.running_ctr.__next__())
    self.retval = self.keystream_buffer[:requested_length]
    self.keystream_buffer = self.keystream_buffer[requested_length:]
    return self.retval

  def encdec(self, b):
    return strxor(self.generate_keystream(len(b)), b)

def __main__():
  cipher = Nonce_CTR_18()
  p = cipher.encdec(base64.b64decode('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='))
  print(p)

if __name__ == '__main__':
  __main__()

