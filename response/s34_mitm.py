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
import socket

class Evil_Bob(socketserver.StreamRequestHandler):
  def handle(self):
    hi_alice = s34_aux.Conn(self)
    p = hi_alice.readnum()
    g = hi_alice.readnum()
    garbo = hi_alice.readnum()

    k = s34_aux.derivekey(0)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 9000))
    bob_socks = s34_aux.Conn(sock)
    bob_socks.sendnum(p)
    bob_socks.sendnum(g)
    bob_socks.sendnum(p)

    garbo = bob_socks.readnum()
    hi_alice.sendnum(p)
    iv = hi_alice.readline()
    ct = hi_alice.readline()
    m = s34_aux.decrypt(k, iv, ct)
    print('Sniffing Alice:\n' + m.decode(), end='\n\n')

    bob_socks.sendline(iv)
    bob_socks.sendline(ct)

    iv = bob_socks.readline()
    ct = bob_socks.readline()
    m = s34_aux.decrypt(k, iv, ct)
    print('Sniffing Bob:\n' + m.decode(), end='\n\n')

    hi_alice.sendline(iv)
    hi_alice.sendline(ct)

def main():
  HOST, PORT = 'localhost', 9001

  socketserver.TCPServer.allow_reuse_address = True
  Bob_with_a_mouSTACHE = socketserver.TCPServer((HOST, PORT), Evil_Bob)

  try:
    Bob_with_a_mouSTACHE.serve_forever()
  except KeyboardInterrupt:
    print('\nCaught evil KeyboardInterrupt. Closing server.')
  except:
    print('EVILEek!')

if __name__ == '__main__':
  main()

