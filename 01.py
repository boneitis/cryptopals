#!/usr/bin/python3

"""
$ perl -e 'print "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d";'|./01.py

"""

import sys
import binascii
import base64

ct_nib = sys.stdin.read( 1024 )
while ct_nib != "":
	print( base64.b64encode(binascii.unhexlify(ct_nib)).decode("utf-8") )
	ct_nib = sys.stdin.read( 1024 )

