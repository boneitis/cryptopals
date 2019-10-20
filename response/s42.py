'''
$ python3 s42.py

Home stretch. Quick and dirty. Don't judge. Sir La Forge certainly doesn't.

'''
import re
from binascii import unhexlify, hexlify
from Crypto.Hash import SHA1
from s40_aux import nthroot

def textbook_rsa_decrypt(c, e, n):
  return pow(c, e, n)

def verify(m, e, n, signature):
  h = SHA1.new(m).hexdigest()
  print('Geordi attempts to verify message:\n ' + m.decode() + '\n..with his calculated hash:\n ' + h)
  decrypt = hexlify(textbook_rsa_decrypt(signature, e, n).to_bytes(128, 'big')).decode()
#  print(decrypt)
  ASN1SHA1 = r'3021300906052b0e03021a05000414'
  r = r'0001(ff)+00' + ASN1SHA1 + r'[0-9A-Fa-f]{20}'
  if re.search(r, decrypt):
    hit = re.search(ASN1SHA1, decrypt)
    h_extract = decrypt[hit.end():hit.end()+40]
    print('..against the extracted hash:\n ' + h_extract, end='\n\n')
    if h_extract == h:
      return True
    else:
      print('Geordi does not verify.')
  else:
    print('Bad Format. Geordi disapproves.')
  return False

if __name__ == '__main__':
  preamble = b'0001'
  m = b'hi mom'
  mom_digest = SHA1.new(m).hexdigest() # 925a89b43f3caff507db0a86d20a2428007f10b6
  goop = b'3021300906052b0e03021a05000414'

  Geordi = preamble + b'ff' + b'00' + goop + mom_digest.encode() + b'0'*178
  LaForge = int(nthroot(3, int.from_bytes(unhexlify(Geordi), 'big'), 200)) + 1

#  print(LaForge)
  if verify(m, 3, LaForge**3 + 1, LaForge):
    print('huzzah')
  else:
    print('kaboom')

