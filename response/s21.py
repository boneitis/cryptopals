'''
$ python3 ./s21.py


'''
  from Crypto.Util.strxor import strxor

  # n = 624
  # w = 32

  int MT[624]
  int index = 625
  lower_mask = b'00000000'
  upper_mask = b'11111111'

  def seed_mt(seed)
    index = 624
    MT[0] = seed
    for i in range(1, index-1):
      MT[i] = 
