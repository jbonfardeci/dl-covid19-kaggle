import json
import os
import re
from pyorient import OrientDB, OrientRecord
from PySocket import PySocket
from typing import Dict, List

"""
Import JSON articles into OrientDB (WIP)
John Bonfardeci
2020-03-26

Run in Python 3.7.3 64-bit env

PyOrient docs - https://orientdb.com/docs/3.0.x/pyorient/PyOrient.html
"""

# change to your instance address and port  
HOST = "localhost"
PORT = 2424
DATABASE_NAME = "Covid19"
DB_USER = "admin"
DB_PWD = "admin"
PAPER_CLUSTER = 21

socket = PySocket(HOST, PORT)
socket.connect()
client = OrientDB(socket)
client.db_open(DATABASE_NAME, DB_USER, DB_PWD) # change to your database name

# change to root folder on your system
dir = "/home/spark/Documents/repos/covid19kaggle/2020-03-13/"

def convert_to_json(contents: str) -> Dict:
    return json.loads(contents)

def read_json(path: str) -> Dict:
    infile = open(path, "r")
    return convert_to_json(infile.read())

def read_files(path: str) -> List:
    file_list = []
    for root, folders, docs in os.walk(path):
        file_list.extend( [os.path.join(root, doc) for doc in docs if '.json' in doc] )

    return file_list

def parse_cluster_id(rid) -> Dict:
    a = rid.split(':')
    return {
        'cluster_id': a[0],
        'id': a[1]
    }
    
def get_rid(record: OrientRecord) -> str:
    return record.__dict__['_OrientRecord__rid']

def upsert_author(auth) -> str:
    middle = 'NULL'
    if len(auth['middle']) > 0:
        middle = ".".join(auth['middle'])

    email = 'NULL'
    if email in auth:
        email = auth['email']

    author = {
        "@Author": {
            "first": auth['first'],
            "middle": middle,
            "last": auth['last'],
            "email": email
        }
    }

    return client.record_create(author)

def insert_bib_entry(paper_id, bib):

    entry = {
        "@BibEntry": {
            "ref_id": bib['ref_id'],
            "paper_id": paper_id,
            "title": bib['title'],
            "year": bib['year'],
            "venue": bib['venue'],
            "issn": bib['issn']
        }
    }
    
    return client.record_create(entry)
    
def insert_paper(data) -> str:
    metadata: str = data['metadata']
    paper_id: str = data['paper_id']
    title: str = metadata['title']
    authors: List = metadata['authors']
    bib_entries: List = data['bib_entries']

    abstracts = []
    for ab in data['abstract']:
        abstracts.append(ab['text'])

    abstract = " ".join(abstracts)

    # Combine all sections in body_text array
    body_text = []
    for section in data['body_text']:
        body_text.append(section['text'])
        # /for

    full_text = " ".join(body_text)

    paper = {
        "@Paper": {
            "paper_id": paper_id,
            "title": title,
            "abstract": abstract,
            "body_text": full_text
        }
    }
   
    record: OrientRecord = client.record_create(PAPER_CLUSTER, paper)

    db_id: str = get_rid(record)

    # authors
    for auth in authors:      
        upsert_author(auth)

    for bibs in bib_entries:
        b = bib_entries[bibs]
        insert_bib_entry(paper_id, b)

    return db_id
    # def


# test_paper = read_json(dir+"biorxiv_medrxiv/biorxiv_medrxiv/0a43046c154d0e521a6c425df215d90f3c62681e.json")
# test_paper_id = insert_paper(test_paper)
# print(test_paper_id)
# client.record_delete(PAPER_CLUSTER, test_paper_id)

# Load JSON articles
docs = read_files(dir)
paper_ids = []

for doc in docs:
    try:
        paper = read_json(doc)
        paper_id = insert_paper(paper)
        paper_ids.append(paper_id)
        rid = parse_cluster_id(paper_id)
        print(rid['id'])
    except:
        print(doc)
        break

print("Imported", len(paper_ids), "documents.")

client.close()