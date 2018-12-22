'''
$ python3 14.py

Getting SUPER lost in the forest.

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
    self.prefix = bytes( [r.randint(0, 255) for x in range(r.randint(1, MAXPREFIXLEN)) ] )
#    self.prefix = b'A'*25
    print('prefix len ' + str(len(self.prefix)))
    self.unknown_string = base64.b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')
    self.random_key = bytes( [r.randint(0, 255) for x in range(self.blocksize)] )
    self.cipher = AES.new( self.random_key, AES.MODE_ECB )

  # return encrypted bytestring of PREFIX||CHOSEN_PT||TARGET_BYTES
  def queryOracle( self, your_string ):
    return self.cipher.encrypt( pad(self.prefix + your_string + self.unknown_string, self.blocksize, style='pkcs7') )

  # SANITY CHECK, verify block index of prefix tail
  def submitPrefixLastBlockIndex( self, lastBlockIndex ):
    return int(len(self.prefix)/self.blocksize) == lastBlockIndex

  # SANITY CHECK, verify sum of lengths of prefix and CPA
#  def submitLenPlusLen( self, lenPlusLen ):
#    return

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

# return minimum buffer length such that CPA causes two buffers to be equal
def findLenStage1( oracle, lbi, bs ):
  x = 0
  while True:
    ct = oracle.queryOracle(b'A'*x)
    if ct[ (lbi+1)*bs:(lbi+1)*bs+bs ] == ct[ (lbi+2)*bs:(lbi+2)*bs+bs ]:
      ctVerify = oracle.queryOracle(b'B'*x)
      # second check with all 'B's to account for false positives resulting from any 'A' in prefix or pt
      if ctVerify[ (lbi+1)*bs:(lbi+1)*bs+bs ] == ctVerify[ (lbi+2)*bs:(lbi+2)*bs+bs ]:
#      return x
        break
      else:
        x += 1
      if x > 3*bs:
        raise Exception('kaboom')
    else:
      x += 1
      if x > 3*bs:
        raise Exception('kaboom')
  return x

def generateKeylist():
  keylist = [ b'\x01', b'\x02', b'\x03', b'\x04', b'\x05', b'\x06', b'\x07', b'\x08', b'\x09', b'\x0a', b'\x0b', b'\x0c', b'\x0d', b'\x0d', b'\x0f', b'\x10' ]
  for k in range(32, 127):
    keylist.append( chr(k).encode() )
  return keylist

def decryptNextByte( oracle, leading_pt, target, keylist, BLOCKSIZE, adjustedBlockIndex, lenStage1 ):
  for key in keylist:
#    print(b'leading pt: ' + leading_pt)
#    print( oracle.queryOracle( leading_pt+key )[:BLOCKSIZE], end='' )
#    print( ' vs ', end='' )
#    print( target )
    if oracle.queryOracle( b'A'*lenStage1 + leading_pt + key )[adjustedBlockIndex*BLOCKSIZE:adjustedBlockIndex*BLOCKSIZE+BLOCKSIZE] == target:
#      print('returns ',end='')
#      print(key)
      return key
  return None
#  print('kaboom')
#  exit(12)


def main():
  gloria = ECB_Oracle()
  blsize = detectBlocksize( gloria )
  print('ECB detected.')
  if detectECB( gloria.queryOracle(b'A'*blsize*3), blsize ):
    print( 'Block size ' + str(blsize) + '.' )
  else:
   raise Exception('kaboom')

  a = blockGenerator( gloria.queryOracle(b'A'), blsize )
  b = blockGenerator( gloria.queryOracle(b'B'), blsize )
  # calculate 'last block index' of prefix
  lbi = 0
  while True:
    if a.__next__() == b.__next__():
      lbi += 1
    else:
      break
  print('prefix lbi is: ' + str(lbi) + ', after: ' + str(lbi*blsize))
  if not gloria.submitPrefixLastBlockIndex(lbi):
    raise Exception( 'Gloria says: Bad block index.' )

  print('so far, so good.')

  lenStage1 = findLenStage1( gloria, lbi, blsize )
  print('lenStage1: ' + str(lenStage1))


  ct = gloria.queryOracle( b'A'*lenStage1 )
  full_ct_len = len(ct) - (lbi + 1 + int(lenStage1 / BLOCKSIZE)) * 16
  print( 'full_ct_len is : ' + str(full_ct_len) + ', ctlen is: ' + str(len(ct)) )
  keylist = generateKeylist()
  r = b'A' * (BLOCKSIZE-1)
  # block index at which target text begins when fuzzed with `lenStage1` bytes
  adjustedBlockIndex = lbi + int(lenStage1/BLOCKSIZE) + 1
  print('adjustedBlockIndex is: ' + str(adjustedBlockIndex))

  i = 0
  blindex = 0
  blockTargets = []
  for byte in range(full_ct_len):
    shift_offset = BLOCKSIZE - 1 - (byte%BLOCKSIZE)
    blockTargets.append( gloria.queryOracle(b'A'*lenStage1 + b'A'*shift_offset)[(adjustedBlockIndex+blindex)*16:(adjustedBlockIndex+blindex)*16 + BLOCKSIZE ] )
    i += 1
    if i % BLOCKSIZE == 0:
      blindex += 1

  for byte in range(full_ct_len):
    leading_pt = r[-BLOCKSIZE+1:]
    nextByte = decryptNextByte( gloria, leading_pt, blockTargets.pop(0), keylist, BLOCKSIZE, adjustedBlockIndex, lenStage1 )
    if nextByte == None:
      r = r[BLOCKSIZE-1:-1]
      break
    else:
      r += nextByte

  print('\nRecovered plaintext:\n\n' + r.decode())

if __name__ == '__main__':
  main()

