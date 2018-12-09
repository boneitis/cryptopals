#!/usr/bin/python3

import sys
import random as r

r.seed()

BLOCKSIZE = 16

RANDIV = bytes( [r.randint(0, 255) for x in range(16)] )
RANDKEY = bytes( [r.randint(0, 255) for x in range(16)] )

def genBytes():
  return bytes( [r.randint(0, 255) for x in range(r.randint(5, 10))] )

prepend = genBytes()
b = prepend + sys.stdin.buffer.read(BLOCKSIZE - len(prepend))
if len(b) == len(prepend)
  print('kaboom')
  exit(11)

while True:
  # block-aligned eof
  if not len(b):
    b = pkcs7Pad( genBytes() )
    AESencrypt()
    break

  # un-aligned eof
  if len(b) != BLOCKSIZE:
    b += pkcs7Pad(b)
    AESencrypt()
    break
  # full block read in
    AESencrypt()

