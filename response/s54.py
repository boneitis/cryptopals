'''
$ python3 s54.py

16-bit hash.
k=8 spacetime tradeoff.

'''

from s53 import f, pad53
#from s54testvectors import testvector5
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes as rand
from Crypto.Random.random import choice
from math import log

K = 8

def iterhash(hashes):
  for Hij in hashes:
    yield Hij

def initialize():
  init = []
  while len(init) < (1 << K):
    h0i = f(rand(16))
    if h0i in init:
      continue
    init.append(h0i)
  return init

def collide54(hleft, hright):
  while True:
    sample0 = rand(16)
    sample1 = rand(16)
    if sample0 == sample1:
      continue
    if f(sample0, hleft) == f(sample1, hright):
      return sample0, sample1

def layercreate(lastlayer):
  hashset = set()
  for hi in lastlayer:
    hashset.add(f(lastlayer[hi], hi))

  h0i = iterhash(hashset)
  li = {}
  length = len(hashset)
  count = 1
  print('\ncolliding layer' + str(8 - int(log(len(hashset), 2))) + ' of 7' + '...')
  while True:
    try:
      hleft = next(h0i)
      try:
        hright = next(h0i)
      except StopIteration:
        ## ADD SENTINEL IN CASE OF 4-COLLISION
        print('MULTICOLLISION ON PREV. LAYER')
        while True:
          hleft = rand(2)
          if hleft not in li:
            break
      mleft, mright = collide54(hleft, hright)
      li[hleft] = mleft
      li[hright] = mright
      print(str(count) + '/' + str(length // 2), end='; ', flush = True)
      count += 1
    except StopIteration:
      break
  return li

def layer0(v0):
  h0i = iterhash(v0)
  l0 = {}
  length = len(v0)
  count = 1
  print('\ncolliding layer0 of 7...')
  while True:
    try:
      hleft = next(h0i)
      hright = next(h0i)
      mleft, mright = collide54(hleft, hright)
      l0[hleft] = mleft
      l0[hright] = mright
      print(str(count) + '/' + str(length // 2), end='; ', flush = True)
      count += 1
    except StopIteration:
      break
  return l0

def build_diamond():
  diamond = []
  diamond.append(layer0(initialize()))
##  diamond.append(testvector0())
  for _ in range(K - 1, 0, -1):
    diamond.append(layercreate(diamond[-1]))
  return diamond

def find_m_link(h2, l0):
  while True:
    m2 = rand(16)
    if f(m2, h2) in l0:
      return m2

def main():
  print('16-bit hash.')
  print('k=8 spacetime tradeoff.', end='\n\n')

  print('building diamond...')
  diamond = build_diamond()
#  diamond = testvector5()
  print('\n')
  print(diamond)

##### MAKE FORECAST #####
  for key in diamond[-1]:
    hashdrop = f(diamond[-1][key], key)
  print('\nh_diamond hashdrop:', hashdrop)

  forecast = choice(open('/usr/share/dict/words', 'r').read().splitlines()).encode()
  forepad = forecast + b' #' + (b'\x00' * (32 - 2 - len(forecast)))
  print('\n\n', forepad)
  h2 = f(forepad)
  print('finding link message')
  m_link = find_m_link(h2, diamond[0])
  print('m_link:', m_link)

  prediction = b''
  prediction += forepad + m_link
  for block in diamond:
    prediction += block[f(prediction)]

  print('\npostseason message:', prediction,'\n\nhash:', f(prediction))
  if f(prediction) == hashdrop:
    print('huzzah')
  else:
    print('kaboom')

if __name__ == '__main__':
  main()

