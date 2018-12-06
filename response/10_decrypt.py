#!/usr/bin/python3

"""
$ tr -d '\n'< challenge/10.txt |base64 -d |./10.py |base64 -d

"""

import sys
from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
from aux import b64sink

KEY = b'YELLOW SUBMARINE'
KEYSZ = len(KEY)
assert( KEYSZ in [16, 24, 32] )
IV = b'\x00' * KEYSZ
assert( len(IV) == KEYSZ )

# implemented or wip so far
assert( KEYSZ in [16] )

cipher = AES.new( KEY, AES.MODE_ECB )

ct = sys.stdin.buffer.read(KEYSZ)
lastCTBlock = IV

if len(ct) != KEYSZ:
  print('kaboom')
  exit(10)

outBuffer = b''

while True:
  if not ct:
    break
  if(len(ct) != KEYSZ):
    print('kaboom')
    exit(11)
  else:
    # append decryption to output buffer
    outBuffer += strxor( cipher.decrypt(ct), lastCTBlock )

    # dequeue b64 block-aligned substring for output
    alignedLength = len(outBuffer) - len(outBuffer)%3
    b64sink( outBuffer[:alignedLength] )
    outBuffer = outBuffer[alignedLength:]

    lastCTBlock = ct
    ct = sys.stdin.buffer.read(KEYSZ)

# flush buffer
b64sink( outBuffer )

