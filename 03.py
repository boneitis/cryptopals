#!/usr/bin/python3

"""
$ perl -e 'print "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736";' |./03.py

Scratch

>>> strxor(b"aaaa", b" ! !")
b'A@A@'
>>> samp = strxor(b"aaaa", b" ! !")
>>> type(samp)
<class 'bytes'>
>>> samp[0]
65
>>> samp[1]
64
>>> samp[2]
65
>>> samp[3]
64


>>> strxor_c(b'aaaa',32)
b'AAAA'


>>> ba.hexlify(b'AAAA')
b'41414141'
>>> hexlified = ba.hexlify(b'4141')
>>> print (hexlified)
b'34313431'

"""

import sys
import binascii
from Crypto.Util.strxor import strxor_c

KEY_CANDIDATE_FLOOR = 0x20
KEY_CANDIDATE_CEIL = 0x7e

# nothing to see here
def scoreCandidate( ptCandidate ):
	localCandidate = ptCandidate.lower().decode("utf-8")
	localScore = 0

	# throw it away if any non-printable ascii in candidate pt
	for x in ptCandidate:
		if( x<0x20 or x>0x7e ):
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

	localScore -= 400 * localCandidate.count('`')
	localScore -= 100 * localCandidate.count('&')
	localScore -= 500 * localCandidate.count('|')

	return localScore;



ct = sys.stdin.read( 10240 )
ct_raw = binascii.unhexlify( ct )

topScore = 0
for key in range( KEY_CANDIDATE_FLOOR, KEY_CANDIDATE_CEIL + 1 ):
	ptCandidate = strxor_c(ct_raw, key)
	currentScore = scoreCandidate( ptCandidate )
	if currentScore > topScore:
		topScore = currentScore
		topCandidate = ptCandidate.decode("utf-8")

# best candidate
print( topCandidate )

