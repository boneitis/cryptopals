'''
$ python3 s52_gthirtytwo.py

Upped the bigger pipewidth to 32 beezies.

'''

from s52_aux import *
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes as rand
#from binascii import hexlify

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

def g(M, H = AES.new(b'YELLOW SUBMARINE', AES.MODE_ECB).encrypt(b'\x21\x43\x54\x87\x80' + (b'\x00' * 11))[:4] + (b'\x80' + b'\x00' * 11)):
  if len(H) < 16:
    H = pad(H, 16, 'iso7816')
  if len(M) % 16 != 0:
    M = pad(M, 16, 'iso7816')
  blocks = []
  for i in range(len(M) // 16):
    blocks.append(M[i*16:(i*16)+16])
  for block in blocks:
    aes = AES.new(H, AES.MODE_ECB)
    H = aes.encrypt(block)[:4] + b'\x80' + (b'\x00' * 11)
  return H[:4]

def collide(M_chain = None):
  while True:
    sample0 = rand(16)
    sample1 = rand(16)
    if sample1 == sample0:
      continue
    if M_chain is not None:
      H_0 = f(sample0, M_chain)
      H_1 = f(sample1, M_chain)
      if H_0 == H_1:
        return [sample0, sample1, f(sample0, M_chain)]
    else:
      H_0 = f(sample0)
      H_1 = f(sample1)
      if H_0 == H_1:
        return [sample0, sample1, f(sample0)]

def main():
  collisions = []
  collisions.append(collide())

  print('pre')
  for b in range(16):
    print('b', b + 1)
    collisions.append(collide(collisions[-1][2]))

  g_calls = 0
  rev_lookup = {}
  for collision in coll65536(collisions):
    g_calls += 1
    lookup = g(collision)
    if lookup not in rev_lookup:
      rev_lookup[lookup] = collision
    else:
      print('found\n', collision, '\n', rev_lookup.get(lookup))
      print('65536-collision: g calls', g_calls, end='\n\n')
      exit()

  print('\n\n65536-collision: g calls', g_calls, end='\n\n')
  print('length', len(rev_lookup))


  g_calls = 0
  rev_lookup = {}
  for collision in coll131072(collisions):
    g_calls += 1
    lookup = g(collision)
    if lookup not in rev_lookup:
      rev_lookup[lookup] = collision
    else:
      print('found\n', collision, '\n', rev_lookup.get(lookup))
      print('131072-collision: g calls', g_calls)
      exit()
                                                                                                                                   
  print('\n\n131072-collision: g calls', g_calls, end='\n\n')
  print('length', len(rev_lookup))


  for collision in collisions:
    print(collision)
  print('\n')

  print('failed to find g-collision.')

#  print('count', trampoline(collisions))



if __name__ == '__main__':
  main()

