'''
s23.py

'''

from s23aux import MT19937

def undo_r18(y):
  return y ^ (y >> 18)

def undo_l15_and_c(y):
  x = y
  y = y ^ ((x << 15) & 0xefc60000)
  return y

def undo_l7_and_b(y):
  x = y
  y = y ^ ((x << 7) & 0x9d2c5680)
  y = y ^ ((x << 14) & 0x94284000)
  y = y ^ ((x << 21) & 0x14200000)
  y = y ^ ((x << 28) & 0x10000000)
  return y

def undo_r11(y):
  return y ^ (y >> 11) ^ (y >> 22)

def untemper(y):
  y = undo_r18(y)
#  print('untempered y3: ' + str(y))
  y = undo_l15_and_c(y)
#  print('untempered y2: ' + str(y))
  y = undo_l7_and_b(y)
#  print('untempered y1: ' + str(y))
  y = undo_r11(y)
  return y

def main():
  r = MT19937()
  r_dupe = MT19937()

  for i in range(624):
    r_dupe.MT.append(untemper(r.extract_number()))
  r_dupe.twist()

  for i in range(100000):
    print('iteration ' + str(i) + '...', end='')
    if r.extract_number() == r_dupe.extract_number():
      print('OK!')
    else:
      print('kaboom')

if __name__ == '__main__':
  main()

