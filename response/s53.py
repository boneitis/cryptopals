'''
$ python3 s52.py


'''

from s52_aux import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes as rand
from Crypto.Random.random import randint
from math import ceil, log

def pad53(M):
  remainder = len(M) % 16
  # normal
  if remainder < 8:
    M += b'\x80' + (b'\x00' * (8 - remainder - 1)) + (len(M)).to_bytes(8, 'big')
  # not enough room
  else:
    M += b'\x80' + (b'\x00' * (16 - remainder - 1 + 8)) + (len(M)).to_bytes(8, 'big')
  return M

def f(M, H = AES.new(b'YELLOW SUBMARINE', AES.MODE_ECB).encrypt(b'\x34\x12\x80' + (b'\x00' * 13))[:2] + (b'\x80' + b'\x00' * 13)):
  if len(H) < 16:
    H = pad(H, 16, 'iso7816')
  if len(M) % 16 != 0:
    M = pad(M, 16, 'iso7816')
  blocks = []
  for i in range(len(M) // 16):
    blocks.append(M[i*16:(i*16)+16])
  for block in blocks:
    aes = AES.new(H, AES.MODE_ECB)
    H = aes.encrypt(block)[:2] + b'\x80' + (b'\x00' * 13)
  return H[:2]

def collide53(M_chain = None, i = None):
  H_0_def = AES.new(b'YELLOW SUBMARINE', AES.MODE_ECB).encrypt(b'\x34\x12\x80' + (b'\x00' * 13))[:2] + (b'\x80' + b'\x00' * 13)
  dummy = (2 ** i) * b'A' * 16
  if M_chain is not None:
    dummychain = f(dummy, M_chain)
  else:
    M_chain = H_0_def
    dummychain = f(dummy)
  while True:
    sample0 = rand(16)
    sample1 = rand(16)
    H_0 = f(sample0, M_chain)
    H_1 = f(sample1, dummychain)
    if H_0 == H_1:
      return [sample0, sample1, H_0, dummychain]

def blockgenerator(paddedbytestring):
  h_interm = AES.new(b'YELLOW SUBMARINE', AES.MODE_ECB).encrypt(b'\x34\x12\x80' + (b'\x00' * 13))[:2] + (b'\x80' + b'\x00' * 13)[2:]
  for block in range(len(paddedbytestring) // 16):
    yield paddedbytestring[block*16:(block*16)+16]

def preimageinterm(H, Hmap):
  while True:
    preimage = rand(16)
    if f(preimage, H) in Hmap:
      return preimage

def main():
  H_0_def = AES.new(b'YELLOW SUBMARINE', AES.MODE_ECB).encrypt(b'\x34\x12\x80' + (b'\x00' * 13))[:2] + (b'\x80' + b'\x00' * 13)

  challengeM = rand(randint(420, 780))
  challengeH = f(pad53(challengeM))
  print('message:\n', challengeM, end='\n\n')
  print('len:', len(challengeM), '\npadded:', len(pad53(challengeM)), end='\n\n')
  print('hash:\n', challengeH, end='\n\n')

  k = ceil(log(len(pad53(challengeM)) // 16, 2))
  print(k, 'blocks k')

  dummy = b'A' * 16
  pool = []
  print('i', k-1)
  pool.append([k-1, collide53(None, k-1)])
  for i in range(k - 2, -1, -1):
    print('i', i)
    pool.append([i, collide53(pool[-1][1][2], i)])

  for collision in pool:
    print(collision)

  H_i_map = {}
  H_i_map[H_0_def[:2]] = 0
  genblocks = blockgenerator(pad53(challengeM))
  count = 1
  H_i = H_0_def[:2]
  for block in genblocks:
    H_i = f(block, H_i)
    H_i_map[H_i] = count
    count += 1
  print('\nintermediates map', H_i_map)

  preimage = preimageinterm(pool[-1][1][2], H_i_map)
  print('\nfound preimage', preimage)
  print('from final expandable state', pool[-1][1][2])
  print('upon entry into block', H_i_map[f(preimage, pool[-1][1][2])], '(', f(preimage, pool[-1][1][2]), ')')

if __name__ == '__main__':
  main()

