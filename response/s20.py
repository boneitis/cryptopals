'''
$ python3 s20.py |./s20aux.py

I'm lazy. Sue me.

'''

import base64
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.strxor import strxor


def generate_ct():
  with open('challenge/20.txt', 'r') as f:
    p = []
    for line in f.read().split('\n'):
      p.append(base64.b64decode(line))

  p.pop(-1)

  retlist = []
  nonce = b'\x00'*8
  key = b'YELLOW SUBMARINE'
  for line in p:
    ctr = Counter.new(64, prefix=nonce, little_endian=True, initial_value=0)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    retlist.append(cipher.encrypt(line))
  return retlist

def __main__():
  c = generate_ct()

  smallest_len = None
  for line in c:
    if smallest_len is None:
      smallest_len = len(line)
    else:
      if len(line) < smallest_len:
        smallest_len = len(line)

  c_cat = b''
  for line in c:
    c_cat += line[:smallest_len]

  print(base64.b64encode(c_cat).decode(), end='')

if __name__ == '__main__':
  __main__()

