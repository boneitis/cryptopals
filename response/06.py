#!/usr/bin/python3

import binascii as ba
import base64 as b64
from s06aux import *

str1 = 'this is a test'
str2 = 'wokka wokka!!!'

hamsum = computeHamming( str1, str2 )
print( hamsum )

rawifiedInput = b64.b64decode('HUIfTQsPAh9PE048GmllH0kcDk4TAQsHThsBFkU2AB4BSWQgVB0dQzNTTmVS').decode()

