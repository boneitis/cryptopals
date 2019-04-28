from s21 import MT19937
import time
from random import randint
import numpy.random

def main():
  time_seed = int(time.time()) + randint(40, 1000)
  rng = numpy.random.RandomState(time_seed)
  pick = rng.randint(0, 2**32)

  r = MT19937()
  my_time = int(time.time())
  for i in range( my_time + 1010, my_time + 30, -1 ):
    r.seed_mt(i)
    my_pick = r.extract_number()
    if my_pick == pick:
      final = i
      break
  print( str(pick) + ' - pick\n' + str(time_seed) + ' - seed\n' + str(i) + ' - my guess' )

  if final == time_seed:
    print('huzzah')
  else:
    print('kaboom')



if __name__ == '__main__':
  main()

