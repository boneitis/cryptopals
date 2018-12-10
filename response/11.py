#!/usr/bin/python3

"""
base64 -d challenge/play.txt |./11_encryption_oracle.py |base64 -d |./11.py

"""

import sys
from aux import b64sink

BLOCKSIZE = 16

def detectECBCBC():
  s = set()
  b = sys.stdin.buffer.read(BLOCKSIZE)
  if b == b'':
    print('kaboom')
    exit(12)
  while b != b'':
    if b in s:
      print('ecb')
      exit(0)
    s.add(b)
    b = sys.stdin.buffer.read(BLOCKSIZE)
  print('cbc suspected')

if __name__ == '__main__':
  detectECBCBC()

