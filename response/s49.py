'''
$ python3 s49.py

'''
from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
from Crypto.Util.Padding import pad, unpad
from Crypto.Random.random import randint
import re

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
    message = pad(b'from=' + str(from_id).encode() + b'&tx_list=' + transactions, 16, 'pkcs7')
    print('message:\n', message.decode(), end='\n\n')
    mac = ciph.encrypt(message)[-16:]
    print('mac\n', mac, end='\n\n')
    return message + mac

  def generate(self, message):
    return AES.new(b'YELLOW SUBMARINE', AES.MODE_CBC, b'\x00'*16).encrypt(message)[-16:]

  def validate(self, messagemac):
    message = messagemac[:-16]
    mac = messagemac[-16:]
    if AES.new(b'YELLOW SUBMARINE', AES.MODE_CBC, b'\x00'*16).encrypt(message)[-16:] == mac:
      return True
    else:
      return False
#    print(macvalidate)

  def process_payments(self, messagemac):
    if self.validate(messagemac):
      toplevellist = re.split(b'&', unpad(messagemac[:-16], 16))
      if toplevellist[0][:5] != b'from=' or toplevellist[1][:8] != b'tx_list=':
        exit(1)
      print('Leela: Processing payments on behalf of account: ' + toplevellist[0][5:].decode())
      for payment in re.split(b';', toplevellist[1][8:]):
        pair = re.split(b':', payment)
        recipient = int(pair[0])
        amount = int(pair[1])
        print('  ' + str(amount) + ' spacebucks for account: ' + str(recipient) + '!!!')

    else:
      print('kaboom')

def main():
  Leela = O49()
  challenge = Leela.challenge()
  print('challenge:\n', challenge)
  print('sanity check')
  if Leela.validate(challenge):
    print('OK')
  else:
    print('panic')
    exit(1)
  print('\n\nattempting forgery...')
  evil = b';666666:1000000'
  tag_new = Leela.generate(strxor(evil + b'\x01', challenge[-16:]))
  print('new tag:', tag_new)
  forgery = challenge[:-16] + evil + b'\x01' + tag_new
  print('forgery:', forgery, end='\n\n')
  Leela.process_payments(forgery)

if __name__ == '__main__':
  main()

