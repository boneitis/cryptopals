'''
$ python3 s31.py

'''

import time
import urllib.request

def recover_next_byte(recovered_bytes):
  hexa = '0123456789abcdef'
  best_time = 100 # sentinel
  for letter in hexa:
    print('polling')
    start = time.perf_counter()
    try:
      r = urllib.request.urlopen('http://localhost:9000/test?file=foo&signature=' + recovered_bytes + letter)
      return letter
    except urllib.error.HTTPError as e:
      end = time.perf_counter()
      if end - start < best_time:
        best_time = end - start
        candidate = letter
  return letter


def main():
  recovered_bytes = ''
  for i in range(40):
    recovered_bytes += recover_next_byte(recovered_bytes)
    print('recovered: ' + recovered_bytes)

if __name__ == '__main__':
  main()

