'''

$ python3 s38_mitm.py
 ..
$ python3 s38.py

'''
import socketserver
import s34_aux
from s36_aux import *
from binascii import unhexlify
from Crypto.Hash import HMAC, SHA256
from Crypto.Random.random import getrandbits, randint

class Handle38(socketserver.StreamRequestHandler):
  def setup(self):
    super().setup()
    self.N = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
    self.g = 2

  def handle(self):
    conn = s34_aux.Conn(self)

    b = randint(2, self.N - 2)
    B = pow(self.g, b, self.N) % self.N

    C_I = conn.readline()
    C_A = conn.readnum()
    conn.sendnum(0)
    conn.sendnum(B)
    conn.sendnum(1)

    target = conn.readline().decode()
    print('Acquired target digest:\n' + target, end='\n\n')
    conn._rfile.close()
    conn._wfile.close()

    with open('challenge/words') as f:
      for password in f:
        print(password.strip(), end=' ')
        x = derive_x(0, password.strip().encode())
        S = pow(C_A * (pow(2, x, self.N)), b, self.N) % self.N
        key_candidate = derive_K(S)
        hash_candidate = HMAC_Wrapper36(key_candidate, 0).hexdigest()
        if hash_candidate == target:
          print('\n\nDictionary lookup successful on target digest:\n' + target + '\n\nPassword:\n' + password)
          return

def main():
  HOST, PORT = 'localhost', 9000
  socketserver.TCPServer.allow_reuse_address = True
  ss = socketserver.TCPServer((HOST, PORT), Handle38)

  try:
    ss.serve_forever()
  except KeyboardInterrupt:
    print('\nCaught KeyboardInterrupt. Closing server.')
  except:
    print('\nEek!')

if __name__ == '__main__':
  main()

