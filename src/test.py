from compress import lz77_compressor

compressor = lz77_compressor(20)

a = 'avavav'

b = compressor.compress(a)
print b
print len(b)