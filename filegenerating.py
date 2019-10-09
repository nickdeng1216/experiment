import sys


file_size = sys.argv[1]
file_name = file_size
file_size = float(file_size)*1024*1024
file_size = int(file_size)
file_name = str(file_size)
f = open(file_name+"B","w+")
f.write(file_size*"t")
f.close()
