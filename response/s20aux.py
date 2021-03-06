#!/usr/bin/python3

"""
cat challenge/6.txt |tr -d '\n' |./06.py
"""

import sys
import binascii as ba
import base64 as b64
from s04aux import *
from s06aux import *

BUFFER_LEN = 4096
KEYSIZE_FLOOR = 53
KEYSIZE_CEIL = 53   # final 40
HAMMING_PAIRS = 7   # final 5
KEYSIZE_TEST_COUNT = 1
#ct = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQ'
ct = b64.b64decode( sys.stdin.buffer.read( BUFFER_LEN ) )

assert( 2*KEYSIZE_CEIL*HAMMING_PAIRS <= len(ct) )
assert( KEYSIZE_TEST_COUNT <= KEYSIZE_CEIL - KEYSIZE_FLOOR + 1)


# { keysize : normedsum }
ksns = {}

for keysize in range( KEYSIZE_FLOOR, KEYSIZE_CEIL+1 ):
    pairOffset = 2 * keysize
    hamSumRaw = 0
    for x in range( HAMMING_PAIRS ):
        hamSumRaw += computeHamming( ct[ (x*pairOffset) : (x*pairOffset)+keysize ], ct[ (x*pairOffset)+keysize : (x*pairOffset)+(2*keysize) ] )
    hamSumNorm = ( float(hamSumRaw) / keysize ) / HAMMING_PAIRS
    ksns[keysize] = hamSumNorm

# print all dic keyval pairs
for x in ksns:
    print(str(x) + ' : ' + str(round(ksns[x],2)))

# fetch keysizes with lowest hamming sums
keysizeCandidates = []
for x in range(KEYSIZE_TEST_COUNT):
    keysizeCandidates.append(sorted(ksns, key=ksns.get)[x])

print( 'ct: ' + str(len(ct)) + ' ' + str(ct) + '\n' )
for x in keysizeCandidates:
    ctListSlice = []
    for i in range(x):
        ctListSlice.append( ct[i::x] )
#        print( str(i) + ' in ' + str(x) )
    for i in range(len(ctListSlice)):
        print(str(len(ctListSlice[i])) + ' ' + str(ctListSlice[i]))
#    if ct %
    print( 'keysize ' + str(x) )
    print( 'singlekeyxor called on: ' )
    somelist = []
    for i in range(len(ctListSlice)):
        somelist.append(breakSingleKeyXOR(ctListSlice[i]))
        print( str(breakSingleKeyXOR(ctListSlice[i])) )
    print( '\n' )

    out = ''
    for i in zip(*somelist):
        for j in i:
            out += chr(j)
    print(out)

