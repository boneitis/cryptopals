'''
$ python3 s40.py

'''

from Crypto.Util.number import getPrime
import numpy
from s39a import extended_gcd as eea, invmod

class RSA_Oracle_40:
  def __init__(self, m):
    if type(m) is int:
      self.m = m
      self.m_len = None
    elif type(m) is bytes:
      self.m = int.from_bytes(m, 'big')
      self.m_len = len(m)
    self.npqs = []                        # 'Ns, Ps, and Qs'
    while len(self.npqs) < 3:
      print('try')
      p = getPrime(512)
      while True:
        q = getPrime(512)
        if q != p:
          break
      et = (p - 1) * (q - 1)
      g, s, t = eea(et, 3)
      if g != 1:
        continue

      if [p * q, p, q] not in self.npqs:
        print('append success')
        self.npqs.append([p * q, p, q])


    self.ds = []                          # 'private decryption key Ds'
    for npq in self.npqs:
      et = (npq[1] - 1) * (npq[2] - 1)
      self.ds.append(invmod(3, et))

    self.cs = []                               # 'ciphertexts'
    self.cs.append(pow(self.m, 3, self.npqs[0][0]))
    self.cs.append(pow(self.m, 3, self.npqs[1][0]))
    self.cs.append(pow(self.m, 3, self.npqs[2][0]))


  def challenge(self):
    challenge_arr = []
    for i in range(3):
      challenge_arr.append([self.cs[i], self.npqs[i][0]])
    return challenge_arr

  def validate_response(self, m_outsider):
    if m_outsider == self.m:
      print('huzzah')
    else:
      print('kaboom')

def main():
  Kelly = RSA_Oracle_40(42)

  c = Kelly.challenge()
  print(c)

  c_0 = c[0][0]
  c_1 = c[1][0]
  c_2 = c[2][0]

  n_0 = c[0][1]
  n_1 = c[1][1]
  n_2 = c[2][1]

  m_s_0 = c[1][1] * c[2][1]
  m_s_1 = c[0][1] * c[2][1]
  m_s_2 = c[0][1] * c[1][1]

  result = (c_0 * m_s_0 * invmod(m_s_0, n_0)) + \
           (c_1 * m_s_1 * invmod(m_s_1, n_1)) + \
           (c_2 * m_s_2 * invmod(m_s_2, n_2))

  m_recovered = numpy.cbrt([result])
  m_recovered = round(m_recovered)
  print('recovered', m_recovered)
  Kelly.validate_response(m_recovered)


if __name__ == '__main__':
  main()

