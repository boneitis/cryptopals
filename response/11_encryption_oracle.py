#!/usr/bin/python3

import sys
import random as r
from Crypto.Cipher import AES
from aux import b64sink

r.seed()

BLOCKSIZE = 16

RANDIV = bytes( [r.randint(0, 255) for x in range(16)] )
RANDKEY = bytes( [r.randint(0, 255) for x in range(16)] )

if r.randint(0, 1):
  sys.stderr.write('oracle: ecb\n')
  cipher = AES.new( RANDKEY, AES.MODE_ECB )
else:
  sys.stderr.write('oracle: cbc\n')
  cipher = AES.new( RANDKEY, AES.MODE_CBC, RANDIV )

def genBytes():
  return bytes( [r.randint(0, 255) for x in range(r.randint(5, 10))] )

def pushBuffer( outBuffer ):
  alignedLength = len(outBuffer) - len(outBuffer)%3
  b64sink( outBuffer[:alignedLength] )
  return outBuffer[alignedLength:]

def pkcs7Pad( nib ):
  difference = BLOCKSIZE - (len(nib) % BLOCKSIZE)
  if difference == 0:
    difference = BLOCKSIZE
  return nib + difference.to_bytes(1, byteorder=sys.byteorder)*difference

prepend = genBytes()
b = prepend + sys.stdin.buffer.read(BLOCKSIZE - len(prepend))

if len(b) == len(prepend):     # fault if nothing read in
  print('kaboom')
  exit(11)

outBuffer = b''

while True:
  # nothing read in, block-aligned eof
  if b == b'':
    b = pkcs7Pad( genBytes() )
    outBuffer += cipher.encrypt(b)
    outBuffer = pushBuffer(outBuffer)
    break

  # un-aligned eof
  if len(b) != BLOCKSIZE:
    b += genBytes()
    b = pkcs7Pad(b)
    if len(b) not in [16, 32]:
      print('kaboom')
      exit(12)
    outBuffer += cipher.encrypt(b)
    outBuffer = pushBuffer(outBuffer)
    break

  # full block read in
  outBuffer += cipher.encrypt(b)
  outBuffer = pushBuffer(outBuffer)

  b = sys.stdin.buffer.read(BLOCKSIZE)

# flush buffer
b64sink(outBuffer)
