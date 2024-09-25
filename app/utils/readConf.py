import os

import toml

def read_conf(file_name):

    if not os.path.exists(file_name):
        print("Файл не найден")

    with open(file_name, 'r') as f:
        config = toml.load(f)
        return config