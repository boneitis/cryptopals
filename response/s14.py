'''
14.py

'''

import sys
import base64
import random as r
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES

r.seed()
BLOCKSIZE = 16
BUFFER = 8000
MAXPREFIXLEN = 500

class ECB_Oracle:
  def __init__( self ):
    self.blocksize = BLOCKSIZE
#    self.prefix = bytes( [r.randint(0, 255) for x in range(MAXPREFIXLEN) ] )
    self.prefix = b'A'*25
    self.unknown_string = base64.b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')
    self.random_key = bytes( [r.randint(0, 255) for x in range(self.blocksize)] )
    self.cipher = AES.new( self.random_key, AES.MODE_ECB )

  # return encrypted bytestring of PREFIX||CHOSEN_PT||TARGET_BYTES
  def queryOracle( self, your_string ):
    return self.cipher.encrypt( pad(self.prefix + your_string + self.unknown_string, self.blocksize, style='pkcs7') )
#    x = self.cipher.encrypt( pad(self.prefix + your_string + self.unknown_string, self.blocksize, style='pkcs7') )
#    print( '\n\n~~~\nencrypting pt, len ' + str(len(x)) + ': ', end='' )
#    print(x,end='')
#    print('\n~~~\n')
#    return x

  # SANITY CHECK, verify block index of prefix tail
  def submitPrefixLastBlockIndex( self, lastBlockIndex ):
    return int(len(self.prefix)/self.blocksize)

  # SANITY CHECK, verify prefix length
  # do we actually need this?
  def submitPrefixLength( self, prefixLen ):
    return len(self.prefix) == prefixLen

def blockLengthGenerator( oracle ):
  fuzzlength = range(33)
  for l in fuzzlength:
    yield len( oracle.queryOracle( b'A'*l ) )

# pass in oracle object; function will fuzz a generator with calls to the oracle to determine block size
def detectBlocksize( oracle ):
  lengths = blockLengthGenerator( oracle )
  initialLength = None
  for l in lengths:
    if initialLength is None:
      initialLength = l
    else:
      if l != initialLength:
        return l-initialLength
  raise Exception('Blocksize exceeds AES maximum keysize. Has ECB been verified?')

def detectECB( ct, blsize ):
  block = 0
  blockSet = set()
  while block * blsize < len(ct):
    if ct[block*blsize:(block*blsize)+blsize] not in blockSet:
      blockSet.add( ct[ block*blsize:(block*blsize)+blsize ] )
    else:
      return True
    block += 1
  return False

def blockGenerator( ct, bs ):
  for byteIndex in range(0, len(ct), bs):
    yield ct[byteIndex:byteIndex+bs]

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
  blsize = detectBlocksize( gloria )
  if detectECB( gloria.queryOracle(b'A'*blsize*3), blsize ):
    print( 'ECB detected, block size ' + str(blsize) + '.' )
  else:
   raise Exception('kaboom')

  a = blockGenerator( gloria.queryOracle(b'A'), blsize )
  b = blockGenerator( gloria.queryOracle(b'B'), blsize )
  x = 0
  while True:
    if a.__next__() == b.__next__():
      break
    else:
      x += 1
  if not gloria.submitPrefixLastBlockIndex(x):
    raise Exception('bad block index')

  print('so far, so good.')

# not needed?
#  if not gloria.submitPrefixLength(25):
#    raise Exception('bad len')



#  ct = gloria.queryOracle( b'' )
#  paddedLen = len(ct)
#  keylist = generateKeylist()
#  r = b'A' * (BLOCKSIZE-1)

#  for byte in range(paddedLen-4):
#    leading_pt = r[-BLOCKSIZE+1:]
#    BLOCKINDEX = int(byte/BLOCKSIZE)
#    offset = BLOCKSIZE - 1 - (byte%BLOCKSIZE)
#    target = gloria.queryOracle( b'A'*offset )[ BLOCKINDEX*BLOCKSIZE : BLOCKINDEX*BLOCKSIZE + BLOCKSIZE ]
#    nextByte = decryptNextByte( gloria, leading_pt, target, keylist, BLOCKSIZE )
#    if nextByte == None:
#      r = r[BLOCKSIZE-1:-1]
#      break
#    else:
#      r += nextByte

#  print(r.decode())

if __name__ == '__main__':
  main()

