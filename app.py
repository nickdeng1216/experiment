import datetime

from flask import Flask
from flask import request
from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json

app = Flask(__name__)

directory = os.getcwd() + os.sep
original_file = directory + 'original'
encrypt_file = directory + 'encrypt'
decrypt_file = directory + 'decrypt'
process_file_path = 'C:' + os.sep + 'share' + os.sep + 'workspace' + os.sep + 'Intercloud' + os.sep + 'retrieve' + os.sep


@app.route('/', methods=['POST'])
def main():
    start_time = datetime.datetime.now()
    raw_content = request.get_data().decode('utf-8')
    content = json.loads(raw_content)
    password = content['password']
    file_name = content['file_name']
    repeat_times = int(content['repeat_times'])
    key = key_generating(password)
    process(file_name, repeat_times, key)
    return_file_name = content['return_file_name']
    data = get_file_content(return_file_name)
    end_time = datetime.datetime.now()
    delta_microseconds = (end_time - start_time).microseconds
    delta_seconds = (end_time - start_time).seconds
    process_time = delta_seconds + delta_microseconds * (10 ** (-6))
    process_time_ms = delta_seconds * 1000 + delta_microseconds * (10 ** (-3))

    return_value = '{"data":"' + data + '", "process_time":"' + str(process_time) + '"}'
    s = 'current_process_time:' + str(process_time_ms)
    print(s)
    return return_value


def get_file_content(file_name):
    f = open(process_file_path + file_name)
    data = f.read()
    f.close()
    return data


@app.route('/save_result', methods=['POST'])
def save_result():
    raw_content = request.get_data().decode('utf-8')
    content = json.loads(raw_content)
    execution_times = content['execution_times']
    process_times = content['process_times']
    process_file_size = content['process_file_size']
    return_file_name = content['return_file_name']
    current_execution_times = content['current_execution_times']
    current_operation_times = content['current_operation_times']
    server_completed = content['server_completed']
    client_completed = content['client_completed']
    current_total_time = content['current_total_time']
    total_time = content['total_time']
    current_round = content['current_round']
    total_round = content['total_round']
    f = open("log.txt", "a+")
    f.write('execution_times:' + execution_times + '\n')
    f.write('process_times:' + process_times + '\n')
    f.write('process_file_size:' + process_file_size + '\n')
    f.write('return_file_name:' + return_file_name + '\n')
    f.write('current_execution_times:' + current_execution_times + '\n')
    f.write('current_operation_times:' + current_operation_times + '\n')
    f.write('server_completed:' + server_completed + '\n')
    f.write('client_completed:' + client_completed + '\n')
    f.write('current_total_time:' + current_total_time + '\n')
    f.write('total_time:' + total_time + '\n')
    f.write('current_round:' + current_round + '\n')
    f.write('total_round:' + total_round + '\n')
    print('total_time:' + total_time)
    return "ok"


'''
data: file need to process
repeat_times: the times of processing
return the zip/unzip result
'''


def process(file_name, repeat_times, key):
    # f = open(process_file_path + file_name)
    # data = f.read()
    # f.close()
    data = get_file_content(file_name)
    # generate_file(original_file, data)

    input_data = bytes(data, 'utf-8')
    for i in range(repeat_times):
        # print(i)
        input_data = encrypt(key, input_data)
    # generate_file(encrypt_file, input_data.decode('utf-8'))

    for i in range(repeat_times):
        # print(i)
        input_data = decrypt(key, input_data)
    return input_data.decode('utf-8')
    # generate_file(decrypt_file, input_data.decode('utf-8'))


def key_generating(password):
    password_provided = password  # This is input in the form of a string
    password = password_provided.encode()  # Convert to type bytes
    salt = b'salt_'  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once


def encrypt(key, input_data):
    return Fernet(key).encrypt(input_data)


def decrypt(key, input_data):
    return Fernet(key).decrypt(input_data)


def generate_file(file_path, data):
    f = open(file_path, "w+")
    f.write(data)
    f.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6161)
