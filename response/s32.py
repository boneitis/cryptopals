'''
$ python3 s32_server.py

Then, from another terminal:

$ python3 s32.py

Warning: Runtime about 30 minutes.

'''

import time
import urllib.request

def recover_next_byte(recovered_bytes):
  hexa = '0123456789abcdef'
  best_time = 0.001 # sentinel
  for letter in hexa:
    raw_time_sum = 0
    for i in range(30):
      start = time.perf_counter()
      try:
        r = urllib.request.urlopen('http://localhost:9000/test?file=foo&signature=' + recovered_bytes + letter + ('f' * (40 - len(recovered_bytes) - 1)))
        return letter
      except urllib.error.HTTPError as e:
        end = time.perf_counter()
        raw_time_sum += (end - start)
#        print(recovered_bytes + letter, raw_time_sum, end - start)
      if raw_time_sum > best_time:
        best_time = raw_time_sum
        candidate = letter
  return candidate


def main():
  recovered_bytes = ''
  for i in range(40):
    recovered_bytes += recover_next_byte(recovered_bytes)
    print('recovered: ' + recovered_bytes)

if __name__ == '__main__':
  main()

