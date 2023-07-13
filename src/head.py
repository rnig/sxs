import sys

chunk = int(sys.argv[1])
ifile = sys.argv[2]
f = open(ifile, encoding='utf-8')
data_read = f.read(chunk)
print(data_read)
f.close()
