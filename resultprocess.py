# import sys

import csv
import re
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import copy

directory = os.getcwd() + os.sep
output_directory = directory + 'output' + os.sep

# file_name = sys.argv[1]
file_path = 'log.txt'
timestamp = re.sub('[^a-zA-Z0-9]', '', str(datetime.now()))
interaction_path = output_directory + 'interaction' + timestamp + '.csv'
operation_path = output_directory + 'operation' + timestamp + '.csv'
mean_file_path = output_directory + 'mean' + timestamp + '.csv'
final_result_path = output_directory + 'final' + timestamp + '.csv'


def process_experiment_result():
    f = open(file_path, "r")
    contents = f.read()
    f.close()
    lst = contents.split('\n')
    number_of_record = 14
    # pattern = '[^a-zA-Z0-9]'
    pattern = '[^a-jl-zA-JL-Z0-9]'
    counter = 0
    output = []
    tmp_list = []
    tmp_tuple = (
        'repeat_times', 'execution_times', 'process_times', 'return_file_size', 'total_time', 'process_file_size',
        'current_execution_times', 'current_operation_times', 'server_completed', 'client_completed',
        'current_process_time', 'current_total_time', 'current_round', 'total_round')
    output.append(tmp_tuple)
    for x in range(len(lst) - 1):
        z = x % number_of_record
        c = x // number_of_record
        if c == counter:
            data = lst[x].split(':')
            if z in (3, 5):
                tmp_list.append(re.sub(pattern, '', data[1]))
            else:
                tmp_list.append(data[1])
            if z == number_of_record - 1:
                counter = counter + 1
                tmp_list[4] = float(tmp_list[4])
                tmp_tuple = tuple(tmp_list)
                # if tmp_tuple[1] == tmp_list[9]:
                output.append(tmp_tuple)
                tmp_list = []
    with open(interaction_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(output)
    df_process = pd.read_csv(interaction_path, usecols=[0, 1, 2, 3, 10])
    df_all = pd.read_csv(interaction_path, usecols=[0, 1, 2, 3, 4, 8, 9])
    gd = df_process.groupby(
        ['repeat_times', 'execution_times', 'process_times', 'return_file_size'])
    df_process_time = gd.aggregate(np.mean)
    df_total_time = df_all[df_all['execution_times'] == df_all['client_completed']]
    df_merge = pd.merge(df_process_time, df_total_time, how='inner',
                        on=['repeat_times', 'execution_times', 'process_times', 'return_file_size'])
    df_merge['total_time'].round(decimals=2)
    df_merge['current_process_time'].round(decimals=2)
    df_merge.to_csv(operation_path)


def mean_experiment_result():
    global df_mean
    df = pd.read_csv(operation_path, usecols=[1, 2, 3, 4, 5, 6],
                     dtype={'repeat_times': int, 'execution_times': int,
                            'process_times': int, 'return_file_size': int, 'current_process_time': float,
                            'total_time': float}, )
    df.columns = ['no_of_iterations_in_mobile', 'no_of_interactions', 'no_of_iterations_in_server',
                  'return_file_size', 'process_time_in_server', 'total_time']
    # df = df[['no_of_iterations_in_mobile', 'no_of_iterations_in_server', 'return_file_size', 'no_of_interactions',
    #          'process_time_in_server', 'total_time']]
    print(df.columns.values)
    for i in range(10):
        max_data = df.groupby(
            ['no_of_iterations_in_mobile', 'no_of_interactions', 'no_of_iterations_in_server', 'return_file_size'])[
                       'total_time'].transform(max) == df['total_time']
        idx = df[max_data].index
        df.drop(idx, inplace=True)
    # for i in range(5):
    #     max_data = df.groupby(
    #         ['no_of_iterations_in_mobile', 'no_of_interactions', 'no_of_iterations_in_server', 'return_file_size'])[
    #                    'total_time'].transform(min) == df['total_time']
    #     idx = df[max_data].index
    #     df.drop(idx, inplace=True)
    # print(df.columns.values)
    gd = df.groupby(
        ['no_of_iterations_in_mobile', 'no_of_iterations_in_server', 'return_file_size', 'no_of_interactions'])
    df_mean = gd.aggregate(np.mean)
    df_mean['total_time'] = df_mean['total_time'].map(lambda x: '%.2f' % (x / 1000))
    df_mean['process_time_in_server'] = df_mean['process_time_in_server'].map(lambda x: '%.2f' % x)
    df_count = df.groupby(['no_of_iterations_in_mobile', 'no_of_iterations_in_server',
                           'return_file_size', 'no_of_interactions']).count()
    df_count.drop('process_time_in_server', axis=1, inplace=True)
    df_merge = pd.merge(df_mean, df_count, how='inner',
                        on=['no_of_iterations_in_mobile', 'no_of_interactions', 'no_of_iterations_in_server',
                            'return_file_size'])
    print(df_merge.columns.values)
    df_merge.to_csv(mean_file_path)
    df_final = pd.read_csv(mean_file_path)
    df_final.to_csv(final_result_path, columns=['no_of_iterations_in_mobile', 'no_of_iterations_in_server',
                                                'return_file_size', 'no_of_interactions', 'total_time_x'])


def start_draw():
    # df = pd.read_csv(output_directory + 'mean20191030070435832402.csv', usecols=[0, 1, 2, 3, 5])
    df = pd.read_csv(final_result_path, usecols=[1, 2, 3, 4, 5])
    print(df.columns.values)
    fields = [['no_of_iterations_in_mobile', 'number of iterations in mobile', [1, 10, 15, 25]],
              ['no_of_iterations_in_server', 'number of iterations in server', [1, 10, 15, 20]],
              ['return_file_size', 'return file size', [100, 500, 1000, 2000]],
              ['no_of_interactions', 'number of interactions', [1, 10, 25, 50]],
              ['total_time', 'time used']]
    df.columns = [fields[0][0], fields[1][0], fields[2][0], fields[3][0], fields[4][0]]
    values = [fields[4][0], fields[4][1]]  # ['total_time', 'time used']
    filter_list = []
    full_collection = [0, 1, 2, 3]
    limit = 4
    for i in range(limit):
        c = i
        flt = []
        c = c + 1
        while c < limit:
            flt = [i, c]
            c = c + 1
            if not all(elem in filter_list for elem in flt):
                filter_list.append(flt)

    final_filter_list = []
    for x in range(len(filter_list)):
        l1 = filter_list[x]
        l2 = list(set(full_collection) - set(l1))
        final_filter_list.append(l1 + l2)
        l2.reverse()
        final_filter_list.append(l1 + l2)

    for i in range(len(final_filter_list)):
        filter0_index = final_filter_list[i][0]
        filter1_index = final_filter_list[i][1]
        axis_index = final_filter_list[i][2]
        legend_index = final_filter_list[i][3]
        filters = [fields[filter0_index], fields[filter1_index]]
        # print('filters:{0}'.format(str(filters)))
        filter0_values = fields[filter0_index][2]  # df.no_of_iterations_in_mobile.unique().tolist()
        filter1_values = fields[filter1_index][2]  # df.no_of_iterations_in_server.unique().tolist()
        axis = [fields[axis_index][0], fields[axis_index][1]]
        legend = [fields[legend_index][0], fields[legend_index][1], fields[legend_index][2]]
        # print('axis={0}, filter0_values={1}, filter1_values={2},\n filters={3}\n, legend={4}, values={5}'.format(
        #     str(axis), str(filter0_values), str(filter1_values), str(filters), str(legend), str(values)))
        draw_graph(axis, df, filter0_values, filter1_values, filters, legend, values)


def draw(df, filters, axis, legend, values):
    # print(filters)
    plt.figure(figsize=(8, 6))
    plt.title(
        'The legend is the {0}.\nTwo filters are the {1}({2}) and the {3}({4}).'.format(
            str(legend[1]), str(filters[0][1]), str(filters[0][2]), str(filters[1][1]), str(filters[1][2])))
    df_process = df[df[filters[0][0]] == int(filters[0][2])]
    df_process = df_process[df_process[filters[1][0]] == int(filters[1][2])]
    df_pivot = pd.pivot_table(df_process, index=[axis[0]], columns=[legend[0]],
                              values=[values[0]], aggfunc='sum')
    plt.ylabel(values[1])
    plt.xlabel(axis[1])
    line = plt.plot(df_pivot, '-o')
    plt.legend(handles=line, labels=legend[2], loc='best')
    plt.savefig(output_directory + filters[0][0] + '_' + str(filters[0][2]) + '_' + filters[1][0] + '_' + str(
        filters[1][2]) + '_' + 'axis_' + str(axis[0]) + '_legend_' + str(legend[0]) + '.png')
    plt.show()


def draw_graph(axis, df, filter0_values, filter1_values, filters, legend, values):
    process_filters = copy.deepcopy(filters)
    for x in range(len(filter0_values)):
        for y in range(len(filter1_values)):
            process_filters[0][2] = filter0_values[x]
            process_filters[1][2] = filter1_values[y]
            draw(df, process_filters, axis, legend, values)


process_experiment_result()
mean_experiment_result()
start_draw()
