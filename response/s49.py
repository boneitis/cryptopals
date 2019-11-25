'''
$ python3 s49.py

'''
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random.random import randint

class O49:
#  def __init__(self):
#    print('O49 init')

  def challenge(self):
    ciph = AES.new(b'YELLOW SUBMARINE', AES.MODE_CBC, b'\x00'*16)
    from_id = randint(100000, 999999)
    transactions = b''
    for i in range( randint(5, 10) ):
      to_id = randint(100000, 999999)
      try:
        assert to_id != from_id
      except AssertionError:
        continue
      if len(transactions) > 0:
        transactions += b';'
      transactions += str(to_id).encode() + b':' + str(randint(1, 99999)).encode()
    if transactions == b'':
      print('panic')
      exit(1)
    message = b'from=' + str(from_id).encode() + b'&tx_list=' + transactions
    print('message:\n', message.decode(), end='\n\n')
    mac = ciph.encrypt(pad(message, 16, 'pkcs7'))[-16:]
    print('mac\n', mac, end='\n\n')
    return message + mac

def main():
  lj = O49()
  challenge = lj.challenge()
  print('challenge:\n', challenge)

if __name__ == '__main__':
  main()

