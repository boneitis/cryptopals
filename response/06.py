#!/usr/bin/python3

import binascii as ba
import base64 as b64
from s06aux import *

#str1 = 'this is a test'
#str2 = 'wokka wokka!!!'
bStr1 = b'this is a test'
bStr2 = b'wokka wokka!!!'

hamsum = computeHamming( bStr1, bStr2 )
print( hamsum )

