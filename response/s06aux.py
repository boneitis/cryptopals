from Crypto.Util.strxor import strxor

def computeHamming( bStr1, bStr2 ):
#    hamstring = int.from_bytes( strxor( str1.encode('ISO-8859-1'), str2.encode('ISO-8859-1')), byteorder='little' )
    hamstring = int.from_bytes( strxor(bStr1, bStr2), byteorder='little' )
    hamsum = 0
    while hamstring:
      hamsum += hamstring & 1
      hamstring = hamstring >> 1
    return hamsum

