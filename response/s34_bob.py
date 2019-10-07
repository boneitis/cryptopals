'''                                                                                               
$ s34_bob.py
  ..
$ s34_mitm.py
  ..
$ s34_alice.py

Much credit again to GH user `akalin for an architectural template

'''

import s34_aux
import socketserver
from Crypto.Random import get_random_bytes
from Crypto.Random.random import randint

class Bob_the_Handler(socketserver.StreamRequestHandler):
  def handle(self):
    conn = s34_aux.Conn(self)
    print('Bob: Received connection.', end='\n\n')

    p = conn.readnum()
    print('Bob: Received p: ' + str(p), end='\n\n')

    g = conn.readnum()
    print('Bob: Received g: ' + str(g), end='\n\n')

    A = conn.readnum()
    print('Bob: Received A: ' + str(A), end='\n\n')

    b = randint(2, p - 2)
    print('Bob: Chose b = ' + str(b), end='\n\n')

    B = pow(g, b, p)
    print('Bob: Derived B = ' + str(B), end='\n\n')

    s = pow(A, b, p)
    print('Bob: Derived shared s = ' + str(s), end='\n\n')

    k = s34_aux.derivekey(s)
    print('Bob: ...and further derived k = ' + str(k), end='\n\n')

    print('Bob: Sending B = ' + str(B), end='\n\n')
    conn.sendnum(B)

    iv = conn.readline()
    c = conn.readline()
    m = s34_aux.decrypt(k, iv, c)
    print('Bob: Received iv, ct.\n' + m.decode(), end='\n\n')

    iv = get_random_bytes(16)
    c = s34_aux.encrypt(k, iv, m)

    print('Bob: Sending iv, ct.', end='\n\n')
    conn.sendline(iv)
    conn.sendline(c)

    print('Bob: Done.\n\n')

def main():
  HOST, PORT = 'localhost', 9000

  socketserver.TCPServer.allow_reuse_address = True
  sexyBob = socketserver.TCPServer((HOST, PORT), Bob_the_Handler)

  try:
    sexyBob.serve_forever()
  except KeyboardInterrupt:
    print('\nCaught KeyboardInterrupt. Closing server.')
  except:
    print('Eek!')


if __name__ == '__main__':
  main()

