import json
import os
from pymongo import MongoClient

"""
Import JSON articles into MongoDB
John Bonfardeci
2020-03-23

Run in Python 3.7.3 64-bit env

PyMongo docs - https://api.mongodb.com/python/current/tutorial.html
"""

# change to root folder on your system
dir = "/home/spark/Documents/repos/covid19kaggle/2020-03-13/"

client = MongoClient('localhost', 27017) # change to your instance address and port
db = client.get_database("covid19") # change to your database name
articles = db['articles'] # change to your collection name

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

# Load JSON articles into MongoDB
docs = read_files(dir)
article_ids = []

for doc in docs:
    article = read_json(doc)
    article_id = articles.insert_one(article).inserted_id
    article_ids.append(article_id)

print("Imported", len(article_ids), "documents.")