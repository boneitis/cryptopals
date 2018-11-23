#!/usr/bin/python3

"""

$ tr -d '\n'< 7.txt |./07.py

"""

import sys
from base64 import b64decode
from Crypto.Cipher import AES

KEY = b'YELLOW SUBMARINE'
B64_PT_BUFFER_LEN = 3840

cipher = AES.new( KEY, AES.MODE_ECB )
ct = b64decode( sys.stdin.buffer.read( B64_PT_BUFFER_LEN ) )
print( cipher.decrypt( ct ).decode( 'ISO-8859-1' ) )

