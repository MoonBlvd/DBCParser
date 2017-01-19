from compress import lz77_compressor
import sys
from bitarray import bitarray

compressor = lz77_compressor(20)

a = '1567FC02000007170D5A'
b = bin(int(a,base = 16))
c = compressor.compress(b[2:])

print b
print c
print len(c)

