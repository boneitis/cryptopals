'''
$ python3 s54.py

16-bit hash.
k=8 spacetime tradeoff.

'''

from s53 import f, pad53
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes as rand
from Crypto.Random.random import choice

def iterhash(hashes):
  for Hij in hashes:
    yield Hij

def initialize():
  init = []
  # change e to 8
  while len(init) < (1 << (2 ** 3)):
    h0i = f(rand(16))
    if h0i in init:
      continue
    init.append(h0i)
  return init
  retlist = []
  i = iterhash(init)
  while True:
    try:
      hleft = next(i)
      hright = next(i)
    except StopIteration:
      break


def collide54(hleft, hright):
  while True:
    sample0 = rand(16)
    sample1 = rand(16)
    if sample0 == sample1:
      continue

def main():
  print('16-bit hash.')
  # fix this before final
  print('k=8 spacetime tradeoff. eventually.', end='\n\n')

  forecast = choice(open('/usr/share/dict/words', 'r').read().splitlines()).encode()

  h0def = AES.new(b'YELLOW SUBMARINE', AES.MODE_ECB).encrypt(b'\x34\x12\x80' + (b'\x00' * 13))[:2] + (b'\x80' + b'\x00' * 13)

  v0 = initialize()
  print(v0)

  outer = []

  hashround = layer(v0)

  for i in range(8 - 1, 0, -1):
    # return 1) list-pair input-chaining-var/message and 2) set output chainingvar
    listpair, nextchainset = layer(i)
    # make sure the invariants end with len(nextchainset) == 1

#  hashes = iterhash(h0)
#  while True:
#    try:
#      hleft = next(hashes)
#      hright = next(hashes)
#      v0.append(collide54(hleft, hright, h0def))
#    except StopIteration:
#      print('layer0 finished')
#      break

#  h1 = []


if __name__ == '__main__':
  main()

