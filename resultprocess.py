# import sys
import csv
import re
from datetime import datetime
import pandas as pd
import numpy as np
import os

directory = os.getcwd() + os.sep
output_directory = directory + 'output' + os.sep
str(datetime.now())
# file_name = sys.argv[1]
file_path = 'log.txt'
output_path = output_directory + 'output' + re.sub('[^a-zA-Z0-9]', '', str(datetime.now())) + '.csv'
final_result_path = output_directory + 'final_result' + re.sub('[^a-zA-Z0-9]', '', str(datetime.now())) + '.csv'
f = open(file_path, "r")
contents = f.read()
f.close()
l = contents.split('\n')
number_of_record = 12
process_record = 30
pattern = "[^a-zA-Z0-9]"


output = []
counter = 0
tmpList = []
tmpTuple = ()

tmpTuple = ('execution_times', 'process_times', 'process_file_size', 'return_file_name', 'current_execution_times',
            'current_operation_times'
            , 'server_completed', 'client_completed', 'current_total_time', 'total_time', 'current_round',
            'total_round')
output.append(tmpTuple)
tmpTuple = []

for x in range(len(l) - 1):
    z = x % number_of_record
    c = x // number_of_record
    if c == counter:
        data = l[x].split(':')
        tmpList.append(re.sub('[^a-zA-Z0-9]', '', data[1]))
        if z == number_of_record - 1:
            counter = counter + 1
            tmpList[9] = float(tmpList[9])
            tmpTuple = tuple(tmpList)
            if tmpTuple[0] == tmpList[7]:
                output.append(tmpTuple)
            # print(tmpTuple)
            tmpList = []

with open(output_path, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(output)

df = pd.read_csv(output_path, usecols=[0, 1, 2, 3, 4, 9],
                 dtype={'execution_times': str, 'process_times': str, 'process_file_size': str,
                        'current_execution_times': str, 'total_time': float},
                 )
gd = df.groupby(['execution_times', 'process_times', 'process_file_size', 'return_file_name'])
gd.aggregate(np.mean).to_csv(final_result_path)
