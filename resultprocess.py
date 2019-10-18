# import sys

import csv
import re
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

directory = os.getcwd() + os.sep
output_directory = directory + 'output' + os.sep

# file_name = sys.argv[1]
file_path = 'log.txt'
timestamp = re.sub('[^a-zA-Z0-9]', '', str(datetime.now()))
interaction_path = output_directory + 'interaction' + timestamp + '.csv'
operation_path = output_directory + 'operation' + timestamp + '.csv'
final_result_path = output_directory + 'mean' + timestamp + '.csv'


def process_experiment_result():
    f = open(file_path, "r")
    contents = f.read()
    f.close()
    lst = contents.split('\n')
    number_of_record = 13
    # pattern = '[^a-zA-Z0-9]'
    pattern = '[^a-jl-zA-JL-Z0-9]'
    counter = 0
    output = []
    tmp_list = []
    tmp_tuple = (
        'repeat_times', 'execution_times', 'process_times', 'return_file_size', 'total_time', 'process_file_size',
        'current_execution_times', 'current_operation_times', 'server_completed', 'client_completed',
        'current_total_time', 'current_round', 'total_round')
    output.append(tmp_tuple)
    for x in range(len(lst) - 1):
        z = x % number_of_record
        c = x // number_of_record
        if c == counter:
            data = lst[x].split(':')
            tmp_list.append(re.sub(pattern, '', data[1]))
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
    df = pd.read_csv(interaction_path)
    df[df['execution_times'] == df['client_completed']].to_csv(operation_path)


def mean_experiment_result():
    global df_mean
    df = pd.read_csv(operation_path, usecols=[1, 2, 3, 4, 5],
                     dtype={'repeat_times': int, 'execution_times': int,
                            'process_times': int, 'return_file_size': int, 'total_time': float}, )
    df.columns = ['no_of_iterations_in_mobile', 'no_of_interactions', 'no_of_iterations_in_server',
                  'return_file_size', 'total_time']
    # for i in range(10):
    #     max_data = df.groupby(
    #         ['no_of_iterations_in_mobile', 'no_of_interactions', 'no_of_iterations_in_server', 'return_file_size'])[
    #                    'total_time'].transform(max) == df['total_time']
    #     idx = df[max_data].index
    #     df.drop(idx, inplace=True)
    # for i in range(5):
    #     max_data = df.groupby(
    #         ['no_of_iterations_in_mobile', 'no_of_interactions', 'no_of_iterations_in_server', 'return_file_size'])[
    #                    'total_time'].transform(min) == df['total_time']
    #     idx = df[max_data].index
    #     df.drop(idx, inplace=True)
    # print(df.columns.values)
    gd = df.groupby(
        ['no_of_iterations_in_mobile', 'no_of_interactions', 'no_of_iterations_in_server', 'return_file_size'])
    df_mean = gd.aggregate(np.mean)
    df_mean['total_time'] = df_mean['total_time'].map(lambda x: x / 1000)
    # df_mean.columns = ['no_of_iterations_in_mobile', 'no_of_interactions', 'no_of_iterations_in_server',
    #                    'return_file_size', 'total_time']
    df_mean.to_csv(final_result_path)


def draw_graph(l_title_key, l_title_value, l_fixed_values, l_line_key, l_line_value, l_x_axis_key, l_x_axis_value,
               l_value_key, l_value_value, l_column_values):
    for y in range(len(l_fixed_values)):
        # print('the {0} round, l_line_value={1}, l_title_value={2}'.format(counter, l_line_value, l_title_value))
        print('The line represents the trends of time cost in different {0}. {1} is {2}'.format(str(l_line_value), str(
            l_title_value), str(l_fixed_values[y])))
        plt.title(
            'The line represents the trends of different {0}\n{1} is set to fixed at {2}'.format(str(l_line_value), str(
                l_title_value), str(l_fixed_values[y])))
        df_process = df_mean[df_mean[l_title_key] == l_fixed_values[y]]
        df_pivot = pd.pivot_table(df_process, index=[l_x_axis_key], columns=[l_line_key],
                                  values=[l_value_key],
                                  aggfunc='sum')
        print(df_pivot.values)
        print(df_pivot.axes)
        plt.ylabel(l_value_value)
        plt.xlabel(l_x_axis_value)
        line = plt.plot(df_pivot, '-o')
        plt.legend(handles=line, labels=l_column_values, loc='best')
        plt.savefig(output_directory + l_title_key + '_' + str(l_fixed_values[
                                                                   y]) + '_' + 'x_axis_' + str(
            l_x_axis_key) + '_line_' + str(l_line_key) + '.png')
        plt.show()


# three conditions
# def draw():
#     plt.figure(figsize=(6.4, 4.8))
#     # counter = 0
#     value_key = 'total_time'
#     value_value = 'Total time(s)'
#     # fixed return_file_size
#     # x axis is execution_times
#     # line is process_times
#     title_key = 'return_file_size'
#     title_value = 'Return file size'
#     fixed_values = df_mean.return_file_size.unique()
#     x_axis_key = 'execution_times'
#     x_axis_value = 'Execution times'
#     line_key = 'process_times'
#     line_value = 'process times'
#     column_values = sorted(df_mean.process_times.unique().tolist())
#     draw_graph(title_key, title_value, fixed_values, line_key, line_value, x_axis_key, x_axis_value, value_key,
#                value_value, column_values)
#     # x axis is process_times
#     # line is execution_times
#     line_key = 'execution_times'
#     line_value = 'execution times'
#     x_axis_key = 'process_times'
#     x_axis_value = 'Process times'
#     column_values = sorted(df_mean.execution_times.unique().tolist())
#     draw_graph(title_key, title_value, fixed_values, line_key, line_value, x_axis_key, x_axis_value, value_key,
#                value_value, column_values)
#     # fixed execution_times
#     # x axis is return_file_size
#     # line is process_times
#     title_key = 'execution_times'
#     title_value = 'Execution times'
#     fixed_values = df_mean.execution_times.unique()
#     x_axis_key = 'return_file_size'
#     x_axis_value = 'Return file size'
#     line_key = 'process_times'
#     line_value = 'Process times'
#     column_values = sorted(df_mean.process_times.unique().tolist())
#     draw_graph(title_key, title_value, fixed_values, line_key, line_value, x_axis_key, x_axis_value, value_key,
#                value_value, column_values)
#     # x axis is process_times
#     # line is return_file_size
#     line_key = 'return_file_size'
#     line_value = 'return file size'
#     x_axis_key = 'process_times'
#     x_axis_value = 'Process times'
#     column_values = sorted(df_mean.return_file_size.unique().tolist())
#     draw_graph(title_key, title_value, fixed_values, line_key, line_value, x_axis_key, x_axis_value, value_key,
#                value_value, column_values)
#     # fixed process_times
#     # x axis is return_file_size
#     # line is execution_times
#     title_key = 'process_times'
#     title_value = 'Process times'
#     fixed_values = df_mean.process_times.unique()
#     x_axis_key = 'return_file_size'
#     x_axis_value = 'Return file size'
#     line_key = 'execution_times'
#     line_value = 'execution times'
#     column_values = sorted(df_mean.process_times.unique().tolist())
#     print('column_values is {0}'.format(column_values))
#     draw_graph(title_key, title_value, fixed_values, line_key, line_value, x_axis_key, x_axis_value, value_key,
#                value_value, column_values)
#     # x axis is execution_times
#     # line is return_file_size
#     line_key = 'return_file_size'
#     line_value = 'return file size'
#     x_axis_key = 'execution_times'
#     x_axis_value = 'Execution times'
#     column_values = sorted(df_mean.return_file_size.unique().tolist())
#     draw_graph(title_key, title_value, fixed_values, line_key, line_value, x_axis_key, x_axis_value, value_key,
#                value_value, column_values)


# four conditions
def draw():
    plt.figure(figsize=(6.4, 4.8))
    # counter = 0
    value_key = 'total_time'
    value_value = 'Total time(s)'
    # fixed return_file_size
    # x axis is execution_times
    # line is process_times
    title_key = 'return_file_size'
    title_value = 'Return file size'
    fixed_values = df_mean.return_file_size.unique()
    x_axis_key = 'execution_times'
    x_axis_value = 'Execution times'
    line_key = 'process_times'
    line_value = 'process times'
    column_values = sorted(df_mean.process_times.unique().tolist())
    draw_graph(title_key, title_value, fixed_values, line_key, line_value, x_axis_key, x_axis_value, value_key,
               value_value, column_values)
    # x axis is process_times
    # line is execution_times
    line_key = 'execution_times'
    line_value = 'execution times'
    x_axis_key = 'process_times'
    x_axis_value = 'Process times'
    column_values = sorted(df_mean.execution_times.unique().tolist())
    # l_title_key, l_title_value, l_fixed_values, l_line_key, l_line_value, l_x_axis_key, l_x_axis_value,
    # l_value_key, l_value_value, l_column_values
    draw_graph(title_key, title_value, fixed_values, line_key, line_value, x_axis_key, x_axis_value, value_key,
               value_value, column_values)
    # fixed execution_times
    # x axis is return_file_size
    # line is process_times
    title_key = 'execution_times'
    title_value = 'Execution times'
    fixed_values = df_mean.execution_times.unique()
    x_axis_key = 'return_file_size'
    x_axis_value = 'Return file size'
    line_key = 'process_times'
    line_value = 'Process times'
    column_values = sorted(df_mean.process_times.unique().tolist())
    draw_graph(title_key, title_value, fixed_values, line_key, line_value, x_axis_key, x_axis_value, value_key,
               value_value, column_values)
    # x axis is process_times
    # line is return_file_size
    line_key = 'return_file_size'
    line_value = 'return file size'
    x_axis_key = 'process_times'
    x_axis_value = 'Process times'
    column_values = sorted(df_mean.return_file_size.unique().tolist())
    draw_graph(title_key, title_value, fixed_values, line_key, line_value, x_axis_key, x_axis_value, value_key,
               value_value, column_values)
    # fixed process_times
    # x axis is return_file_size
    # line is execution_times
    title_key = 'process_times'
    title_value = 'Process times'
    fixed_values = df_mean.process_times.unique()
    x_axis_key = 'return_file_size'
    x_axis_value = 'Return file size'
    line_key = 'execution_times'
    line_value = 'execution times'
    column_values = sorted(df_mean.process_times.unique().tolist())
    print('column_values is {0}'.format(column_values))
    draw_graph(title_key, title_value, fixed_values, line_key, line_value, x_axis_key, x_axis_value, value_key,
               value_value, column_values)
    # x axis is execution_times
    # line is return_file_size
    line_key = 'return_file_size'
    line_value = 'return file size'
    x_axis_key = 'execution_times'
    x_axis_value = 'Execution times'
    column_values = sorted(df_mean.return_file_size.unique().tolist())
    draw_graph(title_key, title_value, fixed_values, line_key, line_value, x_axis_key, x_axis_value, value_key,
               value_value, column_values)


process_experiment_result()
mean_experiment_result()
draw()
