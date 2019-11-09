# import sys
import datetime
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
gray_color_set = ['black', 'lightgrey', 'darkgrey']
mixed = True
graph = 'bar_chart'


# mixed = False


# graph = 'line_graph'


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
    # print(df_merge.columns.values)
    df_merge.to_csv(mean_file_path)
    df_final = pd.read_csv(mean_file_path)
    df_final.to_csv(final_result_path, columns=['no_of_iterations_in_mobile', 'no_of_iterations_in_server',
                                                'return_file_size', 'no_of_interactions', 'total_time_x'])


def draw(df, filters, axis, legend, values):
    df_process = df[df[filters[0][0]] == int(filters[0][2])]
    df_process = df_process[df_process[filters[1][0]] == int(filters[1][2])]
    df_pivot = pd.pivot_table(df_process, index=[axis[0]], columns=[legend[0], 'cloud'],
                              values=[values[0]], aggfunc='sum')
    # print(df_pivot)
    converted_legend = []
    for i in range(len(legend[2])):
        converted_legend.append(str(legend[2][i]) + '-hk')
        if mixed:
            converted_legend.append(str(legend[2][i]) + '-us')
    plt.title(
        'The {1}: {2}\nThe {3}: {4}\nThe legend: {0}'.format(
            str(legend[1]), str(filters[0][1]), str(filters[0][2]), str(filters[1][1]), str(filters[1][2])))
    plt.ylabel(values[1])
    plt.xlabel(axis[1])
    # print(converted_legend)
    if graph == 'line_graph':
        draw_line(df_pivot, converted_legend)
    elif graph == 'bar_chart':
        draw_bar(df_pivot, axis, converted_legend)
    plt.savefig(output_directory + '{0}{1}{2}{3}{4}{5}'.format(str(legend[3]), str(axis[3]), str(filters[0][3]),
                                                               str(filters[1][3]), str(filters[0][2]),
                                                               str(filters[1][2])) + '.png')
    plt.cla()


def draw_line(df_pivot, converted_legend):
    line = plt.plot(df_pivot, '-o')
    plt.legend(handles=line, labels=converted_legend, loc='best')


def draw_bar(df_pivot, axis, converted_legend):
    performance = df_pivot.T.values.tolist()

    name_list = axis[2]
    n = len(name_list)
    total_width = 1.2
    x = [0, 1.3, 2.6]
    l = len(converted_legend)
    width = total_width / l
    for i in range(len(performance)):
        num_list = performance[i]
        plt.bar(x, num_list, width=width, label=converted_legend[i], tick_label=name_list,
                color=[gray_color_set[i % 2]])
        for j in range(n):
            x[j] = x[j] + width

    plt.legend()


def draw_graph(axis, df, filter0_values, filter1_values, filters, legend, values):
    process_filters = copy.deepcopy(filters)
    for x in range(len(filter0_values)):
        for y in range(len(filter1_values)):
            process_filters[0][2] = filter0_values[x]
            process_filters[1][2] = filter1_values[y]
            draw(df, process_filters, axis, legend, values)


def start_draw():
    df = pd.read_csv(output_directory + 'final20191031102401625627 (copy).csv', usecols=[1, 2, 3, 4, 5, 6])
    fields = []
    # if not mixed:
    #     fields = [['no_of_iterations_in_mobile', 'number of iterations in mobile', [1, 10, 15, 25], 'm'],
    #               ['no_of_iterations_in_server', 'number of iterations in server', [1, 10, 15, 20], 's'],
    #               ['return_file_size', 'return file size', [100, 500, 1000, 2000], 'f'],
    #               ['no_of_interactions', 'number of interactions', [1, 10, 25, 50], 'i'],
    #               ['total_time', 'time used'],
    #               ['cloud', 'cloud']]
    # else:
    fields = [['no_of_iterations_in_mobile', 'number of iterations in mobile', [1, 10, 25], 'm'],
              ['no_of_iterations_in_server', 'number of iterations in server', [1, 10, 20], 's'],
              ['return_file_size', 'return file size', [100, 1000, 2000], 'f'],
              ['no_of_interactions', 'number of interactions', [1, 10, 50], 'i'],
              ['total_time', 'time used'],
              ['cloud', 'cloud']]
    df.columns = [fields[0][0], fields[1][0], fields[2][0], fields[3][0], fields[4][0], fields[5][0]]
    values = [fields[4][0], fields[4][1]]
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

    plt.ioff()
    plt.figure(figsize=(8, 6))
    for i in range(len(final_filter_list)):
        filter0_index = final_filter_list[i][0]
        filter1_index = final_filter_list[i][1]
        axis_index = final_filter_list[i][2]
        legend_index = final_filter_list[i][3]
        filters = [fields[filter0_index], fields[filter1_index]]
        filter0_values = fields[filter0_index][2]
        filter1_values = fields[filter1_index][2]
        axis = [fields[axis_index][0], fields[axis_index][1], fields[axis_index][2], fields[axis_index][3]]
        legend = [fields[legend_index][0], fields[legend_index][1], fields[legend_index][2], fields[legend_index][3]]
        draw_graph(axis, df, filter0_values, filter1_values, filters, legend, values)


start = datetime.now()
print(str(start))
# process_experiment_result()
# mean_experiment_result()
start_draw()
end = datetime.now()
print(str(start))
print(end - start)
