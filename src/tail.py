import os
import sys
import time

start = time.time()
chunk = int(sys.argv[1])
ofile = open(sys.argv[3], 'w', encoding="unicode_escape") #"utf-8")
with open(sys.argv[2], 'rb') as f:
    try:  # catch OSError in case of a one line file 
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
    except OSError:
        f.seek(0)
    last_line = f.readline().decode()
    tail_text = last_line[-chunk:]
    ll = len(last_line)
ofile.write(tail_text)
stop = time.time()
delta = stop - start
print(f"After {delta} seconds we counted {ll} characters and the last {chunk} were written to {sys.argv[3]}.")
ofile.close()
