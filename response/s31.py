'''
$ python3 s31.py

'''

from binascii import unhexlify
from Crypto.Random import get_random_bytes
from Crypto.Random.random import randint
from Crypto.Util.strxor import strxor_c
from s29 import SHA1_29

class HMAC_31:
  def __init__(self, key = get_random_bytes(20), m = b'hello world'):
    self.key = key
#   print('key:', self.key)
    self.m = m
#   print('m:', self.m)
    self.hash = SHA1_29()
    self.bs = 64
    self.output_size = 20
    if len(self.key) > self.bs:
      self.key = self.hash.digest(self.key)
    if len(self.key) < self.bs:
#      print('class31: appending', (0).to_bytes((self.bs - len(self.key)), 'little'), 'to key')
      self.key = self.key + (0).to_bytes((self.bs - len(self.key)), 'little')
    self.o_key_pad = strxor_c(self.key, 0x5c)
    self.i_key_pad = strxor_c(self.key, 0x36)
#    print('class31: ipad', self.i_key_pad.hex())
#    print('class31: opad', self.o_key_pad.hex())
#   print(self.hash.digest(self.m).hex())

  def hmac_digest(self):
#    print('class31: inner hash digesting:', self.i_key_pad.hex(), 'cat', self.m)
#    print('class31: outer hash digesting:', self.o_key_pad.hex(), 'cat', self.hash.digest(self.i_key_pad + self.m).hex())
#   print('class31: passing to inner:', (self.i_key_pad + self.m))
    return self.hash.digest(    self.o_key_pad + self.hash.digest(self.i_key_pad + self.m)    )

testvectors = \
[
  [ (0x0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b).to_bytes(20, 'big'),          b'Hi There',                              b'b617318655057264e28bc0b6fb378c8ef146be00' ], \
  [ b'Jefe',                                                                   b'what do ya want for nothing?',          b'effcdf6ae5eb2fa2d27416d5f184df9c259a7c79' ], \
  [ (0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa).to_bytes(20, 'big'),  unhexlify(b'dd' * 50),                            b'125d7342b9ac11cd91a39af48aa17b4f63f175d3' ], \
  [ (0x0102030405060708090a0b0c0d0e0f10111213141516171819).to_bytes(25, 'big'), (b'\xcd' * 50),                          b'4c9007f4026250c6bc8414f9bf50c86c2d7235da' ], \
    # Succeeding line: Digest truncation not implemented
  [ (0x0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c).to_bytes(20, 'big'),  b'Test With Truncation',                          b'4c1a03424b55e07fe7f27be1d58bb9324a9a5a04' ], \
  [ unhexlify(b'aa' * 80),                                   b'Test Using Larger Than Block-Size Key - Hash Key First',  b'aa4ae5e15272d00e95705637ce8a3b55ed402112' ], \
  [ unhexlify(b'aa' * 80),                 b'Test Using Larger Than Block-Size Key and Larger Than One Block-Size Data', b'e8e99d0f45237d786d6bbaa7965c7808bbff1a91' ] \
]
def main():
  for i in testvectors:
    myhmac = HMAC_31(i[0], i[1])
    o = myhmac.hmac_digest()
    print('\nfinalmac:', o.hex())

if __name__ == '__main__':
  main()

