#!/usr/bin/python3

"""
for candidate_keylen in range(2,40+1):
ctListSlice = []
for x in range(candidate_keylen):
  ctListSlice.append( ct[x::candidate_keylen] )
"""

import sys
import binascii as ba
import base64 as b64
#from s04aux import *
from s06aux import *

BUFFER_LEN = 4096
KEYSIZE_FLOOR = 2
KEYSIZE_CEIL = 40
HAMMING_PAIRS = 7
#NO_PT_PER_KEYSIZE = 1
#ct = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
ct = b64.b64decode( sys.stdin.buffer.read( BUFFER_LEN ) ).decode()

assert( 2*KEYSIZE_CEIL*HAMMING_PAIRS <= len(ct) )

# { keysize : normedsum }
ksns = {}

for keysize in range( KEYSIZE_FLOOR, KEYSIZE_CEIL+1 ):
    pairOffset = 2 * keysize
    hamSumRaw = 0
    for x in range( HAMMING_PAIRS ):
#        print( ct[ (x*pairOffset) : (x*pairOffset)+keysize ] + ", " + ct[ (x*pairOffset)+keysize : (x*pairOffset)+(2*keysize) ] )
        hamSumRaw += computeHamming( ct[ (x*pairOffset) : (x*pairOffset)+keysize ], ct[ (x*pairOffset)+keysize : (x*pairOffset)+(2*keysize) ] )
#        print( "keysize " + str(keysize) + ", sum " + str(hamSumRaw) + ", on " + ct[ (x*pairOffset) : (x*pairOffset)+keysize ] + ", " + ct[ (x*pairOffset)+keysize : (x*pairOffset)+(2*keysize) ] )
    hamSumNorm = ( float(hamSumRaw) / keysize ) / HAMMING_PAIRS
# succeeding for loop does same thing
#    print("keysize " + str(keysize) + ", normed sum " + str(round(hamSumNorm,2)))
    ksns[keysize] = hamSumNorm
for x in ksns:
    print(str(x) + ' : ' + str(round(ksns[x],2)))

print( sorted(ksns, key=ksns.get)[0] )
