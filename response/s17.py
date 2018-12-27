'''
s17.py

'''

import sys
from base64 import b64decode
import random as r
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.strxor import strxor

BS = 16
r.seed()
pt_pool = [
            'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
            'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
            'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
            'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
            'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
            'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
            'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
            'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=',
            'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
            'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93'
          ]
#pt_pool = ['YmJiYmJiYmJiYmJiYmJiYmFhYWFhYWFhYWFhYWFhYWE=']          # DELETE ME


class CBC_Oracle_17:

  def __init__(self):
    self.iv = bytes([r.randint(0,255) for x in range(BS)])
#    self.iv = b'\x17'*16                                        # DELETE ME
    self.key = bytes([r.randint(0,255) for x in range(BS)])
#    self.key = b'\x18'*16                                       # DELETE ME
    self.enc_circuit = AES.new(self.key, AES.MODE_CBC, self.iv)
    self.random_pick = r.choice(pt_pool)
    self.ct = self.enc_circuit.encrypt(pad(b64decode(self.random_pick), BS, style = 'pkcs7'))
#    self.ct = self.enc_circuit.encrypt(b64decode(self.random_pick))
    self.dec_circuit = AES.new(self.key, AES.MODE_CBC, self.iv)
    self.dec_circuit.decrypt(self.ct)

  def fetch_iv(self):
    return self.iv

  def fetch_challenge(self):
    print('Challenge: ', end='')
    print(self.ct, end='\n\n')
    print('ct len: ' + str(len(self.ct)))
    return self.ct

  def query(self, b):
    unpad(self.dec_circuit.decrypt(b), BS, style='pkcs7')

  def evaluate_response(self, b):
    print('\n\nJulia says: ', end='')
    if b == b64decode(self.random_pick):
      print('Good.')
    else:
      print('No.')

def generateKeys():
  for k in range(256):
    yield int.to_bytes(k, 1, sys.byteorder)

def decrypt_complement(oracle, ct):
  complement = b''

  for x in range(BS):
    padmask = b'\x00'*(BS-x-1) + int.to_bytes(x+1, 1, byteorder=sys.byteorder) * (x+1)
    keys = generateKeys()
    for k in keys:
      try:
        ct_prev_tamper = strxor(                                                                        \
#                     ((b'z'* (BS-x-1)) + k + complement),                                   \
                     (bytes([r.randint(0,255) for x in range(BS-x-1)]) + k + complement),   \
                     padmask                                                                \
        )
#        print(b'  q: ' + ct_prev_tamper )
        oracle.query(ct_prev_tamper + ct)
#        print(b'key found: ' + k)
        complement = k + complement
        break
      except ValueError:
        continue
    # endfor
#    print('finished outer for iter: ' + str(x))
  # endfor

#  print(b'decrypt returning: ' + complement)
  return complement

def main():
  julia = CBC_Oracle_17()
  ct = julia.fetch_iv() + julia.fetch_challenge()
  # break ct into 16-byte blocks
  ct_blocks = [ct[i:i+BS] for i in range(0, len(ct), BS)]

  for bl in ct_blocks:
    print(bl)
  print('\n\n')

  response = b''
  for i in range(len(ct_blocks)-1, 0, -1):
    response = strxor(decrypt_complement(julia, ct_blocks[i]), ct_blocks[i-1]) + response
#  response = strxor(decrypt_complement(julia, ct_blocks[-1]), ct_blocks[-2]) + response    # first(last) block only

  print('Response:')
  print(unpad(response, BS, style='pkcs7'))
  julia.evaluate_response(unpad(response, BS, style='pkcs7'))


if __name__ == '__main__':
  main()

