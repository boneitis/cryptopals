import socketserver
import s34_aux
from s36_aux import *
from binascii import unhexlify
from Crypto.Hash import HMAC, SHA256
from Crypto.Random.random import getrandbits, randint

class Handle36(socketserver.StreamRequestHandler):
  def setup(self):
    super().setup()
    self.N = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
    self.g = 2
    self.k = 3
    self.I = b'some@handsome.guy'
    self.P = b'totesSecurePW'

  def derive_v(self, salt, P):
    x = derive_x(salt, P)
    return pow(self.g, x, self.N)

  def handle(self):
    conn = s34_aux.Conn(self)

    salt = getrandbits(64)
    v = self.derive_v(salt, self.P)
    b = randint(2, self.N - 2)
    B = ((self.k * v) + pow(self.g, b, self.N)) % self.N

    C_I = conn.readline()
    C_A = conn.readnum()
    conn.sendnum(salt)
    conn.sendnum(B)

    u = derive_u(C_A, B)

    S = pow((C_A * pow(v, u, self.N)), b, self.N)
    K = derive_K(S)
#    print('S: ' + str(S))
#    print('K: ', K)

    h = HMAC_Wrapper36(K, salt)
    response = conn.readline().decode()
    h.auth(response)

def main():
  HOST, PORT = 'localhost', 9000
  socketserver.TCPServer.allow_reuse_address = True
  ss = socketserver.TCPServer((HOST, PORT), Handle36)

  try:
    ss.serve_forever()
  except KeyboardInterrupt:
    print('\nCaught KeyboardInterrupt. Closing server.')
  except:
    print('\nEek!')

if __name__ == '__main__':
  main()

