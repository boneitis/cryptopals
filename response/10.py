#!/usr/bin/python3

"""
$ tr -d '\n'< challenge/10.txt |base64 -d |./10_decrypt.py |base64 -d |./10.py |base64 -d |./10_decrypt.py |base64 -d

ToDo: solutions currently assume block-aligned input. work PKCS#7 into them.

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

pt = sys.stdin.buffer.read(KEYSZ)
lastCTBlock = IV

if len(pt) != KEYSZ:
  print('kaboom')
  exit(10)

outBuffer = b''

while True:
  if not pt:
    break
  if(len(pt) != KEYSZ):
    print('kaboom')
    exit(11)
  else:
    ct = cipher.encrypt( strxor(pt, lastCTBlock) )
    # append decryption to output buffer
    outBuffer += ct
    lastCTBlock = ct

    # dequeue b64 block-aligned substring for output
    alignedLength = len(outBuffer) - len(outBuffer)%3
    b64sink( outBuffer[:alignedLength] )
    outBuffer = outBuffer[alignedLength:]

    pt = sys.stdin.buffer.read(KEYSZ)

# flush buffer
b64sink( outBuffer )

