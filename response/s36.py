'''

$ python3 s36_server.py
 ..
$ python3 s36.py

'''
import socket
from Crypto.Hash import HMAC, SHA256
from Crypto.Random.random import getrandbits, randint
import s34_aux
from s36_aux import *

N = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff

g = 2
k = 3
I = b'some@handsome.guy'
P = b'totesSecurePW'

a = randint(2, N - 2)
A = pow(g, a, N)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 9000))
conn = s34_aux.Conn(sock)

conn.sendline(I)
conn.sendnum(A)

salt = conn.readnum()
B = conn.readnum()

u = derive_u(A, B)
x = derive_x(salt, P)
S = pow((B - (k * pow(g, x, N))),       a + (u * x),       N)
K = derive_K(S)
#print('S: ' + str(S))
#print('K: ', K)

h = HMAC_Wrapper36(K, salt)
tag = h.hexdigest()

conn.sendline(tag.encode())

sock.close()

