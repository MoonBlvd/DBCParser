from compress import lz77_compressor
import sys

compressor = lz77_compressor(20)

a = 'How are you?'
c = compressor.compress(a)
print c
print len(c)
