#!/usr/bin/python3

"""
$ ./02.py <@param1> <@param2>

Todo:
  See about breaking inputs into blocks; is it possible to overwhelm hex()?
"""

import sys

if len( sys.argv ) == 3:
	if len( sys.argv[1] ) != len( sys.argv[2] ):
		print( sys.argv[0] + ": Parameter length mismatch." )
	else:
		xorOut = hex( int(sys.argv[1], 16) ^ int(sys.argv[2], 16) )
		print( xorOut.lstrip("0x").zfill(len(sys.argv[1])) )
elif len( sys.argv ) == 1:
	xorOut = hex( int("1c0111001f010100061a024b53535009181c", 16) ^ \
		int("686974207468652062756c6c277320657965", 16) )
	print( xorOut.lstrip("0x") )
else:
	print( "Usage: " + sys.argv[0] + " <@param1> <@param2>" )

