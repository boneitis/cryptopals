'''                                                                                               
$ s34_bob.py
  ..
$ s35_mitm.py
  ..
$ s35_alice.py

Much credit again to GH user `akalin for an architectural template

'''

import s34_aux
import socket
from Crypto.Random import get_random_bytes
from Crypto.Random.random import randint

for i in range(3):
  p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
  if i == 0:
    g = 1
  elif i == 1:
    g = p
  else:
    g = p-1

  a = randint(2, p - 2)
  A = pow(g, a, p)

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect(('localhost', 9001))

  conn = s34_aux.Conn(sock)

  conn.sendnum(p)
  conn.sendnum(g)
  conn.sendnum(A)

  B = conn.readnum()

  s = pow(B, a, p)

  k = s34_aux.derivekey(s)

  iv = get_random_bytes(16)
  m = b"Rollin' in my 5.0\nWith my rag-top down so my hair can blow\nThe girlies on standby waving just to say hi\nDid you stop? No, I just drove by\n"

  conn.sendline(iv)
  conn.sendline(s34_aux.encrypt(k, iv, m))

  iv = conn.readline()
  c = conn.readline()
  m = s34_aux.decrypt(k, iv, c)

  print('Alice: Received iv, ct.\n' + m.decode(), end='\n\n\n')
  sock.close()
