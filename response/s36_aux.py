from binascii import unhexlify
from Crypto.Hash import HMAC, SHA256

def preprocess(i):
  if len(hex(i)) % 2 == 0:
    return unhexlify(hex(i)[2:].encode())
  else:
    return unhexlify(b'0' + hex(i)[2:].encode())

def deprocess(b):
  return int.from_bytes(b, 'big')

def derive_u(A, B):
  uH = SHA256.new(preprocess(A) + preprocess(B)).digest()
  return deprocess(uH)

def derive_x(salt, P):
  xH = SHA256.new(preprocess(salt) + P).digest()
  x = int.from_bytes(xH, 'big')
  return x

def derive_K(S):
  return SHA256.new(preprocess(S)).digest()

class HMAC_Wrapper36():
  def __init__(self, K, salt):
    self.h = HMAC.new(K, preprocess(salt), digestmod=SHA256)

  def hexdigest(self):
    return self.h.hexdigest()

  def auth(self, tag):
    print('Verifying...', end='')
    try:
      self.h.hexverify(tag)
      print('Smooth.')
    except ValueError:
      print('Failed to authenticate.')
    
