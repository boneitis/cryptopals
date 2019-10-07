'''                                                                                               
$ s34_bob.py
  ..
$ s34_mitm.py
  ..
$ s34_alice.py

Much credit again to GH user `akalin for an architectural template

'''

import socket
import socketserver
from binascii import hexlify, unhexlify
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA1

class Conn:
  def __init__(self, fd):
    if isinstance(fd, socket.socket):
      f = fd.makefile(mode = 'rwb', buffering = 0)
      self._rfile = f
      self._wfile = f
    elif isinstance(fd, socketserver.StreamRequestHandler):
      self._rfile = fd.rfile
      self._wfile = fd.wfile
    else:
      raise Exception('Eek!')

  def readline(self):
    return b64decode(self._rfile.readline().strip())

  def sendline(self, m):
    self._wfile.write(b64encode(m) + b'\n')

  def readnum(self):
    return int(self._rfile.readline().strip())

  def sendnum(self, num):
    self._wfile.write(str(num).encode() + b'\n')

def derivekey(s):
  s = hex(s)[2:].encode()
  if len(s) % 2 != 0:
    s = b'0' + s
  return SHA1.new(unhexlify(s)).digest()[:16]

def encrypt(k, iv, m):
  cipher = AES.new(k, AES.MODE_CBC, iv)
  return cipher.encrypt(pad(m, 16, 'pkcs7'))

def decrypt(k, iv, c):
  cipher = AES.new(k, AES.MODE_CBC, iv)
  return unpad(cipher.decrypt(c), 16, 'pkcs7')

