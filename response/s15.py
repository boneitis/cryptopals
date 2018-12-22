'''
$ python3 s15.py

'''

def validate_and_unpad_pkcs7(b):
  for byte in range(b[-1]):
    if b[-1-byte] != b[-1]:
      raise Exception('PKCS#7 verification: Bad padding.')
  return b[ :len(b)-b[-1] ]

def main():
  print(validate_and_unpad_pkcs7(b'ICE ICE BABY\x04\x04\x04\x04'))
#  print(validate_and_unpad_pkcs7(b'ICE ICE BABY\x05\x05\x05\x05'))
  print(validate_and_unpad_pkcs7(b'ICE ICE BABY\x01\x02\x03\x04'))

if __name__ == '__main__':
  main()

