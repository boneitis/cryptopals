#!/usr/bin/python3

import sys
import binascii as ba

try:
  nib = sys.stdin.read(8)
except:
  print('kaboom')
  exit(9)

while True:
  if nib == '':
    print('\x08'*8, end='')
    break

  length = len(nib)
  if length == 8:
    print(nib, end='')
    nib = sys.stdin.read(8)
  else:
    nib += ( ba.unhexlify('{:02}'.format(8-length))*(8-length) ).decode()
    print(nib, end='')
    break

