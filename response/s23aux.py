'''
$ python3 ./s21.py


'''

class MT19937:
  def __init__(self):
    self.w = 32
    self.n = 624
    self.m = 397
    self.r = 31
    self.MT = []
    self.index = self.n + 1
    self.lower_mask = (1 << self.r) - 1
    self.upper_mask = 1 << self.r

    self.a = 0x9908b0df
    self.f = 1812433253
    self.u = 11
    self.d = (1 << 32) - 1
    self.s = 7
    self.b = 0x9d2c5680
    self.t = 15
    self.c = 0xefc60000
    self.l = 18

  def seed_mt(self, seed):
#    self.MT = []
    self.index = self.n
    self.MT.append(seed)
    self.low_32_mask = (1 << 32) - 1
    for i in range(1, self.n):
      self.MT.append(self.low_32_mask & (self.f * (self.MT[i-1] ^ (self.MT[i-1] >> (self.w-2))) + i))

  def extract_number(self):
    if self.index >= self.n:
      if self.index > self.n:
        # Reference C default if generator has not been seeded
        self.seed_mt(5489)
      self.twist()

    self.y = self.MT[self.index]
#    print(self.y)
    self.y = self.y ^ ((self.y >> self.u) & self.d)
#    print('internal y1:   ' + str(self.y))
    self.y = self.y ^ ((self.y << self.s) & self.b)
#    print('internal y2:   ' + str(self.y))
    self.y = self.y ^ ((self.y << self.t) & self.c)
#    print('internal y3:   ' + str(self.y))
    self.y = self.y ^ (self.y >> self.l)

    self.index += 1
    return ((1 << self.w) - 1) & self.y


  def twist(self):
    for i in range(self.n):
      self.x = (self.MT[i] & self.upper_mask) + (self.MT[(i+1) % self.n] & self.lower_mask)
      self.xA = self.x >> 1
      if (self.x % 2) != 0:
        self.xA = self.xA ^ self.a
#      print('i=' + str(i) + ' + m=' + str(self.m) + ' % n=' + str(self.n))
      self.MT[i] = self.MT[(i + self.m) % self.n] ^ self.xA
    self.index = 0

def main():
  r = MT19937()
  for x in range(1000):
    print(str(r.extract_number()))

if __name__ == '__main__':
  main()

'''
w=32: word size (in number of bits)
n=624: degree of recurrence
m=397: middle word, an offset used in the recurrence relation defining the series x, 1 ≤ m < n
r=31: separation point of one word, or the number of bits of the lower bitmask, 0 ≤ r ≤ w=32 - 1
a=\x9908b0df: coefficients of the rational normal form twist matrix
b=\x9d2c5680, c=\xefc60000: TGFSR(R) tempering bitmasks
s=7, t=15: TGFSR(R) tempering bit shifts
u=11, d=\xffffffff, l=18: additional Mersenne Twister tempering bit shifts/masks

'''
