#!/usr/bin/python3

from s06aux import *

str1 = 'this is a test'
str2 = 'wokka wokka!!!'

hamsum = computeHamming( str1.encode('ISO-8859-1'), str2.encode('ISO-8859-1') )
print( hamsum )

