'''
import base64
from Crypto.Cipher import AES
from Crypto.Util import Counter

nonce = b'\x00'*8
ctr = Counter.new(64, prefix=nonce, little_endian=True, initial_value=0)
key = b'YELLOW SUBMARINE'
c = base64.b64decode('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==')
cipher = AES.new(key, AES.MODE_CTR, counter=ctr)


p = cipher.decrypt(c)


(1).to_bytes(8, byteorder='little')

'''
