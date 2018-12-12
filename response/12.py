#!/usr/bin/python3

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
    self.random_key = b'YELLOW SUBMARINE'
#    self.random_key = bytes( [r.randint(0, 255) for x in range(self.blocksize)] )
    self.cipher = AES.new( self.random_key, AES.MODE_ECB )

  # return encrypted bytestring of your_string||unknown_string
  def queryOracle( self, your_string ):
    return self.cipher.encrypt( pad(your_string + self.unknown_string, self.blocksize, style='pkcs7') )

  # remove first byte of pt, return number of remaining bytes
  def consumeByte():
    self.unknown_string = self.unknown_string[1:]
    return len( self.unknown_string )

def lengthGenerator():
  lengthList = range(33)
  
def detectBlocksize( oracleObject ):
  lengthGenerator = len( oracleObject.queryOracle
  initialLength = len( oracleObject.queryOracle(b'') )
  for x in range(1, 33):
    iterateLength = oracleObject.queryOracle( b'A' * x )
  return 16

def detectECB( pt ):
  return True

def main():
  gloria = ECB_Oracle()
  BLOCKSIZE = detectBlocksize( gloria )
  ct = gloria.queryOracle( b'' )
  b64sink(ct)
  print()

if __name__ == '__main__':
  main()

