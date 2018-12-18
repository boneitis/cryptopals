import string
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import random as r
r.seed()

class ECB_Oracle:
  def __init__( self ):
    self.blocksize = 16
    self.random_key = bytes( [r.randint(0, 255) for x in range(self.blocksize)] )
    self.cipher = AES.new( self.random_key, AES.MODE_ECB )

  def queryOracle( self, challenge ):                                                                                    
    return self.cipher.encrypt( pad(challenge, self.blocksize, style='pkcs7') )

  # parse string into raw, 'processable' object
  def kvparse(self, s):
    s1 = s.split('&')
    s2 = []
    for x in s1:
      s2.append( x.split('=') )
    return s2

  def decrypt_and_parse( self, ct ):
    pt = unpad( self.cipher.decrypt(ct), self.blocksize, style='pkcs7' )
    return self.kvparse( pt.decode() )

# encode from raw model data
def stitch( profile ):
  stitch = []
  for x in profile:
    stitch.append( x[0] + '=' + str(x[1]) )
  profileOut = '&'.join(stitch)

  return profileOut

def profile_for( email ):
  # sanitize, then create default profile in raw, 'processable' form
  email = email.replace('&', '').replace('=', '')
  profile = []
  profile.append( ['email', email] )
  profile.append( ['uid', 10 ] )
  profile.append( ['role', 'user' ] )

  # send to stitch() for encoding, and return
  return stitch(profile)


def main():
  mary = ECB_Oracle()
  query1 = mary.queryOracle( profile_for('foo@bar.coadmin' + '\x0b'*11).encode() )
  query2 = mary.queryOracle( profile_for('foo@bar.commm').encode() )

  submit = query2[:32] + query1[16:32]
  print( stitch( mary.decrypt_and_parse(submit) ))

if __name__ == '__main__':
  main()

