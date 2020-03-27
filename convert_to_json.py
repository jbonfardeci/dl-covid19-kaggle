import json
import os

dir = "/home/spark/Documents/repos/covid19kaggle/2020-03-13/"
target = dir+"converted/"

def convert_to_json(contents):
    return json.loads(contents)

def read_json(path):
    infile = open(path, "r")
    return convert_to_json(infile.read())

def read_files(path):
    file_list = []
    for root, folders, docs in os.walk(path):
        file_list.extend( [os.path.join(root, doc) for doc in docs if '.json' in doc] )

    return file_list

file_list = read_files(dir)

i = 0
for file_path in file_list:
    path = file_path.replace(dir, target)
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.makedirs(folder)

    contents = read_json(file_path)
    f = open(path, "a")
    f.write(str(contents))
    i += 1

print("Converted", i, "documents.")