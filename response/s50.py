from binascii import hexlify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.strxor import strxor

def main():
  m = b"alert(\'MZA who was that?\');\n"
  k = b'YELLOW SUBMARINE'
  c = AES.new(k, AES.MODE_CBC, b'\x00' * 16).encrypt(pad(m, 16, 'pkcs7'))
  c_target = c[-16:]
  chaining_var = c[-32:-16]
  pt_block = pad(m, 16, 'pkcs7')[-16:]
  preimage = strxor(chaining_var, pt_block)

  print('targeting CBC-MAC:\n  ' + hexlify(c_target).decode())
  print('preimage:\n  ' + hexlify(preimage).decode(), end='\n\n')

  forgery = b"alert('Ayo, the Wu is back!');\n//" + (b' ' * 15)
  forgery += strxor(AES.new(k, AES.MODE_CBC, b'\x00' * 16).encrypt(forgery)[-16:], preimage)
  cbcmac = AES.new(k, AES.MODE_CBC, b'\x00' * 16).encrypt(forgery)[-16:]
  print('forgery:\n  ', forgery, end='\n\n')

  if cbcmac == c_target:
    print('huzzah')

if __name__ == '__main__':
  main()

