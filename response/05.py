#!/usr/bin/python3

"""
$ perl -e 'print "Burning \x27em, if you ain\x27t quick and nimble\nI go crazy when I hear a cymbal";' |./05.py
"""

import sys
import argparse as ap
from Crypto.Util.strxor import strxor
import binascii as ba

parser = ap.ArgumentParser()
parser.add_argument( '-k', '--key', help='set ASCII key' )
parser.add_argument( '-bs', '--buffer-size', help='set buffer size', type=int )
args = parser.parse_args()

if args.key:
    KEY = args.key.encode()
else:
    KEY = b'ICE'
if args.buffer_size:
    BUF_LIMIT = args.buffer_size
else:
    BUF_LIMIT = 1024

MOD_OPERAND = len(KEY)
BUF_LIMIT_ALIGNED = BUF_LIMIT - (BUF_LIMIT % MOD_OPERAND)
assert BUF_LIMIT_ALIGNED > 0
assert MOD_OPERAND <= BUF_LIMIT_ALIGNED

#print( 'key is: ' + KEY.decode('ISO-8859-1') )
#print( 'key length is: ' + str( MOD_OPERAND ) )
#print( 'bs is: ' + str(BUF_LIMIT) )

pt = sys.stdin.buffer.read(BUF_LIMIT_ALIGNED)
while pt != b'':
    mod_pad = len(pt) % MOD_OPERAND
    KEY_REPEATED = (KEY * int(len(pt)/MOD_OPERAND)) + KEY[:mod_pad]
#    print(" key repeated: " + KEY_REPEATED.decode('ISO-8859-1') )
    print( ba.hexlify(strxor(pt, KEY_REPEATED)).decode('ISO-8859-1'), end='' )
    pt = sys.stdin.buffer.read(BUF_LIMIT_ALIGNED)
