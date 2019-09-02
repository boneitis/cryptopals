'''
s24.py

'''

from s21 import MT19937
import random
import time
from Crypto.Util.strxor import strxor

class MTCipher:

  def __init__(self):
    self.rng = MT19937()
#    self.fetch32 = self.rng.extract_number()
#    self.imod = 0
    self.rbits = random.Random()

  def next_byte(self):
    self.imod += 1
    retval = 0xff & (self.fetch32 >> (8 * (self.imod - 1)))

    if self.imod == 4:
      self.fetch32 = self.rng.extract_number()
      self.imod = 0

    return retval

  def generate_keystream(self, length, seed=None):
    assert(length > 0)
    if seed:
      self.seed = seed
      self.rng.seed_mt(self.seed)
    else:
      self.seed = self.rbits.getrandbits(16)
      self.rng.seed_mt(self.seed)
    self.fetch32 = self.rng.extract_number()
    self.imod = 0
    keystream = b''
    for i in range(length):
      keystream += self.next_byte().to_bytes(1, 'little')
    print('returning keystream: ', end='')
    print(keystream)
    return keystream

  def challenge_known_pt(self):
    prefix_length = self.rbits.randint(2, 32)
    prefix = self.rbits.getrandbits(8 * prefix_length).to_bytes(prefix_length, 'little')
    known_pt = b'A' * 14
    pt = prefix + known_pt
    print('challenge pt: ', end='')
    print(pt, end='\n\n')
    retval = strxor(pt, self.generate_keystream(len(pt)))
    print('returning challenge: ', end='')
    print(retval, end='\n\n')
    return retval

  def challenge_reset_token(self):
    self.token_pt = b''
    for i in range(20):
      self.token_pt += self.rbits.randint(32, 126).to_bytes(1, 'little')
    seed = int(time.time())
    keystream = self.generate_keystream(len(self.token_pt), seed)
    challenge = strxor(self.token_pt, keystream)

    print('token oracle: \n  plaintext: ', end='')
    print(self.token_pt)
    print('  keystream: ', end='')
    print(keystream)
    print('  challenge: ', end='')
    print(challenge)

    return challenge

  def verify_token(self, response):
    print('token oracle says: ', end='')
    if response == self.token_pt:
      print('huzzah')
    else:
      print('kaboom')

def main():
  norah = MTCipher()
  challenge = norah.challenge_known_pt()
  length = len(challenge)
  print('challenge: ', end='')
  print(challenge)

  aux_cipher = MTCipher()
  for i in range((2<<15)-1):
    print('key: ', end='')
    print(i)
    test = strxor(challenge, aux_cipher.generate_keystream(length, i))
#    if strxor(challenge, aux_cipher.generate_keystream(length, i))[-14:] == b'A' * 14:
    if test[-14:] == b'A' * 14:
      print('key found: ', end='')
      print(i)
      break

  print('test: ', end='')
  print(test)
  print('challenge: ', end='')
  print(challenge)
  print('oracle seed: ' + str(norah.seed))

  challenge = norah.challenge_reset_token()

  print('main, challenge: ', end='')
  print(challenge)

  response_seed = int(time.time())
  response = strxor(aux_cipher.generate_keystream(len(challenge), response_seed), challenge)
  norah.verify_token(response)

if __name__ == '__main__':
  main()

