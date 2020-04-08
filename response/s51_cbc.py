'''
$ python3 s51_cbc.py

'''
from Crypto.Util import Counter
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes as rand
from Crypto.Random.random import randint
from Crypto.Random.random import choice
from zlib import compress as zcomp

class O51:
  def __init__(self):
    self.a = b'hi'

  def format_request(self, P):
    return b'POST / HTTP/1.1\n' + \
           b'Host: hapless.com\n' + \
           b'Cookie: sessionid=TmV2ZXIgcmV2ZWFsIHRoZSBXdS1UYW5nIFNlY3JldCE=\n' + \
           b'Content-Length: ' + str(len(P)).encode() + b'\n' + \
           P

  def compress(self, req):
    return zcomp(req)

  def encrypt(self, creq):
#    ctr = Counter.new(64, prefix = rand(8), little_endian=True, initial_value = randint(0, (2 << 31) - 1))
    return AES.new(rand(16), AES.MODE_CBC, rand(16)).encrypt(pad(creq, 16, 'pkcs7'))

  def query(self, P):
#    print('dorothea: returning ' + str(len(self.encrypt(self.compress(self.format_request(P))))))
    return len(self.encrypt(self.compress(self.format_request(P))))

  def challenge(self, response):
    if response == b'TmV2ZXIgcmV2ZWFsIHRoZSBXdS1UYW5nIFNlY3JldCE=':
      print('huzzah')
    else:
      print('kaboom')

def brutebyte(dorothea, alpha, wip):
  randbytes = b''
  thebyte = b''
  while True:
    minimum = 100000
    lengths = []
    for byte in alpha:
      workingmin = dorothea.query(wip + byte.to_bytes(1, 'big') + randbytes)
      lengths.append(workingmin)
      if workingmin < minimum:
        minimum = workingmin
        thebyte = byte
        print('found min', minimum, 'from byte', thebyte.to_bytes(1, 'big'))
#    print('lengths', lengths, 'minimum', minimum, 'arrsize', len(lengths))
    if lengths.count(minimum) != 1:
      randbytes += choice(b'!@#$%^&*()_').to_bytes(1, 'big')
      continue
    return thebyte.to_bytes(1, 'big')


'''
  if len(alpha) == 1:
    return alpha
  if len(alpha) % 2 != 0:
    alpha += b'_'

  mid = len(alpha) // 2
  left = b''
  for letter in alpha[:mid:]:
    left += wip + letter.to_bytes(1, 'big')
  right = b''
  for letter in alpha[mid::]:
    right += wip + letter.to_bytes(1, 'big')
  print('  bouncing', left, '\n  and', right)

  while dorothea.query(left) == dorothea.query(right):
    randByte = rand(1)
    left += randByte
    right += randByte

  if dorothea.query(left) < dorothea.query(right):
    print('recursing LEFT on', alpha[:mid])
    return brutebyte(dorothea, alpha[:mid], wip)
  else:
    if alpha[-1] == 95:
      alpha = alpha[:-1]
    print('recursing RIGHT on', alpha[mid:])
    return brutebyte(dorothea, alpha[mid:], wip)
'''

def main():
  alpha = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
  base = b'sessionid='
  dorothea = O51()

  movingalpha = alpha
  for secret in range(44):
    base += brutebyte(dorothea, alpha, base)
    print(base)

  dorothea.challenge(base[10:])

if __name__ == '__main__':
  main()

