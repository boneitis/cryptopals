from Crypto.Util.strxor import strxor

def computeHamming( str1, str2 ):
    hamstring = int.from_bytes( strxor( str1.encode('ISO-8859-1'), str2.encode('ISO-8859-1')), byteorder='little' )
    hamsum = 0
    while hamstring:
      hamsum += hamstring & 1
      hamstring = hamstring >> 1
    return hamsum

