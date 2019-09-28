'''
$ python3 s31_server.py

Then, from another terminal:

$ python3 s31.py

Much credit to GH user `akalin` and their solutions as supplemental material for web/sockets refresher.

'''

from binascii import hexlify, unhexlify
from Crypto.Random import get_random_bytes
from Crypto.Random.random import randint
from Crypto.Util.strxor import strxor_c
import time
import socketserver
import http.server
from urllib import parse
from s29 import SHA1_29

#RUNTIMEKEY = (0x0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b).to_bytes(20, 'big')
RUNTIMEKEY = get_random_bytes(20)

def generate_foo():
  rand_len = randint(1, 100)
  s = b''

  for i in range(rand_len):
    s += randint(32, 126).to_bytes(1, 'little')

  f = open('foo', 'w')
  f.write(s.decode('utf-8'))
  f.close()

class Handler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    validated = False
    print('raw path:', self.path)
    u = parse.urlparse(self.path)
    if u.path == '/test':
      q = parse.parse_qs(u.query)
      if 'file' in q and 'signature' in q and q['file'][0] == 'foo' and len(q['signature'][0]) == 40:
        f = open('foo', 'rb')
        m = f.read(256)
        f.close()
        hmac = HMAC_31(key = RUNTIMEKEY)
        checksum = hexlify(hmac.hmac_digest(m)).decode('utf-8')
        print('Target signature: ' + (' ' * 17) + checksum)
        validated = self.insecure_compare(checksum, q['signature'][0])
    if validated == True:
      self.send_error(200)
    else:
      self.send_error(500)

  def insecure_compare(self, a, b):
    for i, j in zip(a.lower(), b.lower()):
      if i == j:
        pass
      else:
        return False
      time.sleep(0.05)
    return True

class HMAC_31:
  def __init__(self, key):
    self.key = key
#    self.m = b'Hi There'
    self.hash = SHA1_29()
    self.bs = 64
    self.output_size = 20
    if len(self.key) > self.bs:
      self.key = self.hash.digest(self.key)
    if len(self.key) < self.bs:
      self.key = self.key + (0).to_bytes((self.bs - len(self.key)), 'little')
    self.o_key_pad = strxor_c(self.key, 0x5c)
    self.i_key_pad = strxor_c(self.key, 0x36)
#    self.foo_digest = self.hash.digest(self.key + readFileFoo)

  def hmac_digest(self, m):
#    print('class31: inner hash digesting:', self.i_key_pad.hex(), 'cat', self.m)
#    print('class31: outer hash digesting:', self.o_key_pad.hex(), 'cat', self.hash.digest(self.i_key_pad + self.m).hex())
#   print('class31: passing to inner:', (self.i_key_pad + self.m))
    return self.hash.digest(    self.o_key_pad + self.hash.digest(self.i_key_pad + m)    )

#  def authenticate_file_request(self, fname, signature):
#    f = open('foo', 'rb')
#    m = f.read(256)
#    validator = HMAC_31()
#    sig_calculated = validator.digest(m)


testvectors = \
[
  [ 1, (0x0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b).to_bytes(20, 'big'),          b'Hi There',                              b'b617318655057264e28bc0b6fb378c8ef146be00' ], \
  [ 2, b'Jefe',                                                                   b'what do ya want for nothing?',          b'effcdf6ae5eb2fa2d27416d5f184df9c259a7c79' ], \
  [ 3, (0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa).to_bytes(20, 'big'),  unhexlify(b'dd' * 50),                            b'125d7342b9ac11cd91a39af48aa17b4f63f175d3' ], \
  [ 4, (0x0102030405060708090a0b0c0d0e0f10111213141516171819).to_bytes(25, 'big'), (b'\xcd' * 50),                          b'4c9007f4026250c6bc8414f9bf50c86c2d7235da' ], \
    # Succeeding line: Digest truncation not implemented
  [ 5, (0x0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c).to_bytes(20, 'big'),  b'Test With Truncation',                          b'4c1a03424b55e07fe7f27be1d58bb9324a9a5a04' ], \
  [ 6, unhexlify(b'aa' * 80),                                   b'Test Using Larger Than Block-Size Key - Hash Key First',  b'aa4ae5e15272d00e95705637ce8a3b55ed402112' ], \
  [ 7, unhexlify(b'aa' * 80),                 b'Test Using Larger Than Block-Size Key and Larger Than One Block-Size Data', b'e8e99d0f45237d786d6bbaa7965c7808bbff1a91' ] \
]
def main():
#  for a, b, c, d in testvectors:
#    print('Test case #' + str(a) + ': ', end='')
#    myhmac = HMAC_31(b, c)
#    o = myhmac.hmac_digest()
#    if o == unhexlify(d):
#      print('huzzah')
#    else:
#      print('kaboom')

  generate_foo()

  HOST, PORT = 'localhost', 9000

  socketserver.TCPServer.allow_reuse_address = True
  ss = socketserver.TCPServer((HOST, PORT), Handler)
  try:
    ss.serve_forever()
  except KeyboardInterrupt:
    print('\nCaught KeyboardInterrupt. Closing server.')
    ss.server_close()
  except:
    print('Eek!')

if __name__ == '__main__':
  main()

