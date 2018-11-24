#!/usr/bin/python3

KEYSIZE_FLOOR = 2
KEYSIZE_CEIL = 7
HAMMING_PAIRS = 3

ct = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP'
assert( 2*KEYSIZE_CEIL*HAMMING_PAIRS <= len(ct) )

for keysize in range( KEYSIZE_FLOOR, KEYSIZE_CEIL+1 ):
    pairOffset = 2 * keysize
    for x in range( HAMMING_PAIRS ):
        print( ct[ (x*pairOffset) : (x*pairOffset)+keysize ] + ", " + ct[ (x*pairOffset)+keysize : (x*pairOffset)+(2*keysize) ] )

