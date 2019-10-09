# import sys
import csv

# file_name = sys.argv[1]
file_path = 'log.txt'
f = open(file_path, "r")
contents = f.read()
f.close()
l = contents.split('\n\n')
transfer_times = 10
number_of_record = 6
rfoxy = transfer_times * number_of_record

print(len(l))

output = []
counter = 0
tmpList = []
tmpTuple = ()

for x in range(len(l)-1):
    z = x % 6
    c = x // 6
    print('x:' + str(x))
    if c == counter:
        data = l[x].split(':')
        tmpList.append(data[1])
        if z == 5:
            counter = counter + 1
            tmpTuple = tuple(tmpList)
            output.append(tmpTuple)
            tmpList = []

with open('output.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(output)
