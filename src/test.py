from compress import lz77_compressor
import sys
from bitarray import bitarray

compressor = lz77_compressor(20)

a = 'hello world!'
b = bitarray(a)
c = compressor.compress(a)
print c
print len(c)
print b[1]
