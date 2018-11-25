#!/usr/bin/python3

"""
Helper for 06, edited from 04.

"""

import sys
import binascii
from Crypto.Util.strxor import strxor_c

KEY_CANDIDATE_FLOOR = 0x00
KEY_CANDIDATE_CEIL = 0xff

def scoreCandidate( ptCandidate ):
#  localCandidate = ptCandidate.lower().decode("utf-8")
    localCandidate = ptCandidate.lower().decode("ISO-8859-1")
    localScore = 0

    for x in ptCandidate:
      if( (x<0x20 and x!=0xa) or x>0x7e ):
        return 0

    localScore += 1202 * localCandidate.count('e')
    localScore += 910 * localCandidate.count('t')
    localScore += 812 * localCandidate.count('a')
    localScore += 768 * localCandidate.count('o')
    localScore += 731 * localCandidate.count('i')
    localScore += 695 * localCandidate.count('n')

    localScore += 628 * localCandidate.count('s')
    localScore += 602 * localCandidate.count('r')
    localScore += 592 * localCandidate.count('h')
    localScore += 432 * localCandidate.count('d')
    localScore += 398 * localCandidate.count('l')
    localScore += 288 * localCandidate.count('u')

    localScore += 271 * localCandidate.count('c')
    localScore += 261 * localCandidate.count('m')
    localScore += 230 * localCandidate.count('f')
    localScore += 211 * localCandidate.count('y')

    localScore += 210 * localCandidate.count(' ')

    localScore += 209 * localCandidate.count('w')
    localScore += 203 * localCandidate.count('g')
    localScore += 182 * localCandidate.count('p')
    localScore += 149 * localCandidate.count('b')
    localScore += 111 * localCandidate.count('v')

    localScore += 69 * localCandidate.count('k')
    localScore += 17 * localCandidate.count('x')
    localScore += 11 * localCandidate.count('q')
    localScore += 10 * localCandidate.count('j')
    localScore += 7 * localCandidate.count('z')

#    localScore -= 200 * localCandidate.count('`')
#    localScore -= 100 * localCandidate.count('&')
#    localScore -= 300 * localCandidate.count('|')

    return localScore;

def breakSingleKeyXOR( ct_raw )
    topScore = 0
#    ct = sys.stdin.buffer.read(4000)
#    ct_raw = binascii.unhexlify( ct )

    for key in range( KEY_CANDIDATE_FLOOR, KEY_CANDIDATE_CEIL + 1 ):
        ptCandidate = strxor_c(ct_raw, key)
        currentScore = scoreCandidate( ptCandidate )
        if currentScore > topScore:
          topScore = currentScore
          topCandidate = ptCandidate

# best candidate
# print( topCandidate.decode("ISO-8859-1") )
    return topCandidate

