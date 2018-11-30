#!/usr/bin/python3
"""
cat challenge/8.txt |./08.py
"""

import fileinput as f
from collections import defaultdict
from pprint import pprint

lineIndex = 0
sumsDict = {}

for line in f.input():
  lineIndex += 1
  inLineStringDict = defaultdict(int)

  # using current block as dict-key, add 1 to the dict-val
  x = 0
  while x < len(line)-16:
    inLineStringDict[line[x:x+16]] += 1
    x += 16

  # sum up all occurrences in the current line
  lineSum = 0
  for y in inLineStringDict:
    if inLineStringDict[y] > 1:
      lineSum += inLineStringDict[y]
  sumsDict[lineIndex] = lineSum
  if lineIndex == 133:
    pprint( inLineStringDict )

longestLineIndex = 0
highSum = 0

for high in sumsDict:
  if sumsDict[high] > highSum:
    highSum = sumsDict[high]
    longestLineIndex = high

print( 'longestLineIndex=' + str(longestLineIndex) )

