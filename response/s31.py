'''
$ python3 s31.py

Then, from another terminal:

$ python3 s31.py

'''

import time
import urllib.request

def recover_next_byte(recovered_bytes):
  hexa = '0123456789abcdef'
  best_time = 0.001 # sentinel
  for letter in hexa:
    start = time.perf_counter()
    try:
      r = urllib.request.urlopen('http://localhost:9000/test?file=foo&signature=' + recovered_bytes + letter + ('f' * (40 - len(recovered_bytes) - 1)))
      return letter
    except urllib.error.HTTPError as e:
      end = time.perf_counter()
#      print('time elapsed on error:', e.code, end-start, 'vs best time', best_time)
      if end - start > best_time:
#        print('inner branch is hit on letter ' + letter)
        best_time = end - start
        candidate = letter
  return candidate


def main():
  recovered_bytes = ''
  for i in range(40):
    recovered_bytes += recover_next_byte(recovered_bytes)
    print('recovered: ' + recovered_bytes)

if __name__ == '__main__':
  main()

