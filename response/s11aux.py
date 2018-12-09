#!/usr/bin/python3
"""
# set BLOCKSIZE = 20
perl -e 'print "YELLOW SUBMARINE";' |./09.py |base64 -d |hexdump -C

"""

import sys
import binascii as ba
from aux import b64sink

# per cryptopals-09 problem description
BLOCKSIZE = 16
# per RFC 2315
assert(BLOCKSIZE > 0 and BLOCKSIZE < 256)

try:
  nib = sys.stdin.buffer.read(BLOCKSIZE)
except:
  print('kaboom')
  sys.exit(9)

while True:
  # pt is BS-aligned, generate full dummy pad
  if nib == '':
    b64sink(int(BLOCKSIZE).to_bytes(1, byteorder=sys.byteorder)*BLOCKSIZE)
    break

  # full BS read in, continue
  length = len(nib)
  if length == BLOCKSIZE:
    b64sink(nib)
    nib = sys.stdin.buffer.read(BLOCKSIZE)

  # not BS-aligned; pad and terminate
  else:
    b64sink( nib + (BLOCKSIZE-length).to_bytes(1, byteorder=sys.byteorder)*(BLOCKSIZE-length) )
    break

