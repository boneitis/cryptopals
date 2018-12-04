"""
Export bytestring/array data in base-64.
Do take care to pass in 3-byte-aligned input until EOF.
"""

import base64 as b64

B64BLOCKSIZE = 1023

assert(B64BLOCKSIZE%3 == 0)

def b64sink(bytesString):
  for x in range( 0, len(bytesString), B64BLOCKSIZE ):
    print( b64.b64encode( bytesString[x:x+B64BLOCKSIZE] ).decode(), end='' )

