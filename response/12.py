'''
12.py

ToDo: Stop being lazy and implement the rest of the problem.
  - Determine block size
  - Detect ECB

Other notes:
  - Assuming I have understood the oracle problem definition properly, the padding should be constantly changing.
  - As far as termination conditions are concerned, with regard to the above, laze is bliss.

'''

import sys
import base64
import random as r
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from aux import b64sink

r.seed()
BUFFER = 6000

class ECB_Oracle:
  def __init__( self ):
    self.blocksize = 16
    self.unknown_string = base64.b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')
#    self.random_key = b'YELLOW SUBMARINE'
    self.random_key = bytes( [r.randint(0, 255) for x in range(self.blocksize)] )
    self.cipher = AES.new( self.random_key, AES.MODE_ECB )

  # return encrypted bytestring of your_string||unknown_string
  def queryOracle( self, your_string ):
    return self.cipher.encrypt( pad(your_string + self.unknown_string, self.blocksize, style='pkcs7') )

# Implement me!
def detectBlocksize( oracleObject ):
#  lengthGenerator = len( oracleObject.queryOracle(b'') )
#  initialLength = len( oracleObject.queryOracle(b'') )
#  for x in range(1, 33):
#    iterateLength = oracleObject.queryOracle( b'A' * x )
  return 16

# Implement me!
def detectECB( pt ):
  return True
    
def generateKeylist():
  keylist = [ b'\x01', b'\x02', b'\x03', b'\x04', b'\x05', b'\x06', b'\x07', b'\x08', b'\x09', b'\x0a', b'\x0b', b'\x0c', b'\x0d', b'\x0d', b'\x0f', b'\x10' ]
  for k in range(32, 127):
    keylist.append( chr(k).encode() )
  return keylist

def decryptNextByte( oracle, leading_pt, target, keylist, BLOCKSIZE ):
  for key in keylist:
#    print(b'leading pt: ' + leading_pt)
#    print( oracle.queryOracle( leading_pt+key )[:BLOCKSIZE], end='' )
#    print( ' vs ', end='' )
#    print( target )
    if oracle.queryOracle( leading_pt+key )[:BLOCKSIZE] == target:
      return key
  return None
#  print('kaboom')
#  exit(12)


def main():
  gloria = ECB_Oracle()
  BLOCKSIZE = detectBlocksize( gloria )
  ct = gloria.queryOracle( b'' )
  paddedLen = len(ct)
  keylist = generateKeylist()
  r = b'A' * (BLOCKSIZE-1)

  for byte in range(paddedLen-4):
    leading_pt = r[-BLOCKSIZE+1:]
    BLOCKINDEX = int(byte/BLOCKSIZE)
    offset = BLOCKSIZE - 1 - (byte%BLOCKSIZE)
    target = gloria.queryOracle( b'A'*offset )[ BLOCKINDEX*BLOCKSIZE : BLOCKINDEX*BLOCKSIZE + BLOCKSIZE ]
    nextByte = decryptNextByte( gloria, leading_pt, target, keylist, BLOCKSIZE )
    if nextByte == None:
      r = r[BLOCKSIZE-1:-1]
      break
    else:
      r += nextByte

  print(r.decode())

if __name__ == '__main__':
  main()

