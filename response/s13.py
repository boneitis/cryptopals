import string
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import random as r
r.seed()

def kvparse(s):
  s1 = s.split('&')
  s2 = {}
  for x in range( len(s1) ):
    s2[s1[x].split('=')[0]] = s1[x].split('=')[1]
  return s2

class ECB_Oracle:
  def __init__( self ):
    self.blocksize = 16
    self.random_key = bytes( [r.randint(0, 255) for x in range(self.blocksize)] )
    self.cipher = AES.new( self.random_key, AES.MODE_ECB )

  def queryOracle( self, challenge ):                                                                                    
    return self.cipher.encrypt( pad(challenge, self.blocksize, style='pkcs7') )

  def decrypt_and_parse( self, ct ):
    pt = unpad( self.cipher.decrypt(ct), self.blocksize, style='pkcs7' )
    return kvparse( pt.decode() )

def profile_for( email ):
  # sanitize
  email = email.replace('&', '').replace('=', '')

  profile = []
  profile.append( ['email', email] )
  profile.append( ['uid', 10 ] )
  profile.append( ['role', 'user' ] )

  stitch = []
  for x in profile:
    stitch.append( x[0] + '=' + str(x[1]) )
  profileOut = '&'.join(stitch)

  return profileOut


def main():
  mary = ECB_Oracle()
  query1 = mary.queryOracle( profile_for('foo@bar.coadmin' + '\x0b'*11).encode() )
#  print(query1)
  query2 = mary.queryOracle( profile_for('foo@bar.commm').encode() )
#  print(query2)
  submit = query2[:32] + query1[16:32]
  print(  mary.decrypt_and_parse(submit) )

if __name__ == '__main__':
  main()

