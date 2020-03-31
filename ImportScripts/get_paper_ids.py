import json
import os
import pandas as pd

dir = "/home/spark/Documents/repos/covid19kaggle/2020-03-13/"

def read_files(path):
    file_list = []
    for root, folders, docs in os.walk(path):
        file_list.extend( [[os.path.basename(doc).replace(".json", "")] for doc in docs if '.json' in doc] )

    return file_list

paper_ids = read_files(dir)

df = pd.DataFrame(columns=['paper_id'], data=paper_ids)
df.to_csv(dir+'json_paper_ids.csv')