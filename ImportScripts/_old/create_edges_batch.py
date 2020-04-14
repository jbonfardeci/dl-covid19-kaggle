import json
import os
import re
import hashlib
from pyorient import OrientDB, OrientRecord
from PySocket import PySocket
from typing import Dict, List
import pandas as pd
import math
import sys
sys.path.append('/home/spark/Documents/repos/dl-covid19-kaggle-contest/Model/')
from covid19_classes import Journal, Paper, Author, Institution, Affiliation, AuthoredBy, PublishedBy, Citation

"""
Import JSON articles into OrientDB (WIP)
John Bonfardeci
2020-03-26

Run in Python 3.7.3 64-bit env

PyOrient docs - https://orientdb.com/docs/3.0.x/pyorient/PyOrient.html
"""

# change to your params
HOST = "localhost"
PORT = 2424
DATABASE_NAME = "Covid19Dev"
DB_USER = "admin"
DB_PWD = "admin"

#vertex clusters
JOURNAL_CLUSTER = 21 # 'JournalCluster'
PAPER_CLUSTER = 22 #'PaperCluster'
AUTHOR_CLUSTER = 23 # 'AuthorCluster'
INSTITUTION_CLUSTER = 24 # 'InstitutionCluster'
# edge clusters
PUBLISHEDBY_CLUSTER = 25 # 'PublishedByCluster'
AUTHOREDBY_CLUSTER = 26 # 'AuthoredByCluster'
AFFILIATION_CLUSTER = 27 # 'AffiliationCluster'
CITATION_CLUSTER = 28 # 'CitationCluster'

FOLDER = "/home/spark/Documents/repos/covid19kaggle/2020-03-13/"

# Open DB connection
socket = PySocket(HOST, PORT)
socket.connect()
client = OrientDB(socket)
client.db_open(DATABASE_NAME, DB_USER, DB_PWD)

def is_iter(o):
    try:
        iter(o)
        return True
    except:
        return False

def to_bool(s):
    rx = re.match("^(1|true|yes)$", trim(str(s).lower()))
    if rx:
        return rx.group() in ['1', 'yes', 'true']

    return False
    
def is_rid(rid:str) -> bool:
    if rid == None:
        return False

    rx = re.match("^#\d+:\d+$", rid)
    if rx:
        return rx.group() == rid 

    return False

def trim(s) -> str:
    return re.sub("(^s\+|\s+$)", "", str(s))

def is_empty(s) -> bool:
    return s == None or s == 'NULL' or trim(s) == '' 

def clean_str(s:str) -> str:
    if s == None or str(s) == 'nan':
        return None

    s = re.sub("[^a-zA-Z0-9\s.-_#:,]", "", str(s))
    return None if len(s) == 0 else s

def to_int(s:str) -> int:
    try:
        n = int(clean_str(s))
        return n
    except:
        return None

def hash_author(author:Dict) -> str:

    def _in(prop:str, o) -> str:
        return trim(o[prop]) if prop in o else ''

    f = _in('first', author)
    l = _in('last', author)
    m = _in('middle', author)
    s = _in('suffix', author)
    e = _in('email', author)

    combined = str.format("{0}{1}{2}{3}{4}", f, l, m, s, e)
    hashed = hashlib.md5(combined.encode())
    return hashed.hexdigest()

def hash_strings(strings:List) -> str:
    a = [trim(s) for s in strings if not is_empty(s)]
    return hashlib.md5(''.join(a).encode()).hexdigest()

def authors_to_list(s:str) -> List:
    """
    Parse the different list types of authors in CSV data.
    """
    s = str(s)

    def _to_dict(s):
        if s == None:
            return {} 

        if s.find(',') > -1:
            names = list( map(trim, s.split(',')) )
            return {
                "first": names[1],
                "last": names[0]
            }

        return {
            "first": None,
            "last": trim(s)
        }

    def _to_json(s):
        try:
            return json.loads(s)
        except json.decoder.JSONDecodeError:
            print(s)
            return []

    if s == None or len(trim(s)) == 0:
        return []

    if s.find("[") > -1:
        s = re.sub("[^\[\]a-z0-9A-Z\.\-\'\"\,\s]", "", s)
        s = s.replace("['", "[\"")
        s = s.replace("', '", "\", \"")
        s = s.replace("']", "\"]")
        s = s.replace("\", '", "\", \"")
        s = s.replace("', \"", "\", \"")
        s = s.replace("']", "\"]")
        s = s.replace(", None", "")
        s = s.replace("']", "\"]")
        s = s.replace("\\xa0", " ")
        s = s.replace("None, ", "")
        s = s.replace("['", "[\"")
        
        lst = _to_json(s)
        return list( map(_to_dict, lst) )

    elif s.find(";") > -1:
        return list( map(_to_dict, s.split(';')) )
    else:
        return [_to_dict(s)]
    
    return s

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

def create_affiliation_edge(institution_hash:str, author_hash:str) -> str:
    return str.format("CREATE EDGE Affiliation FROM (SELECT FROM Institution WHERE institution_hash='{0}') TO (SELECT FROM Author WHERE hash_id='{1}')", )
    
def create_citation_edges(paper_id:str, bib:Dict):

    def _create(paper_id:str, author_hash:str) -> str:      
        return str.format("CREATE EDGE Citation FROM (SELECT FROM Paper WHERE paper_id='{0}') TO (SELECT FROM Author WHERE hash_id='{1}')", paper_id, author_hash)

    sql = []
    for author in bib['authors']:
        author_hash = hash_author(author)
        sql.append(_create(paper_id, author_hash))

    return sql
    
def create_authoredby_edge(paper_id:str, author_hash_id:str) -> str:
    return str.format("CREATE EDGE AuthoredBy FROM (SELECT FROM Paper WHERE paper_id='{0}') TO (SELECT FROM Author WHERE hash_id='{1}')", paper_id, author_hash_id)

def create_publishedby_edge(journal_name:str, paper_id:str):
    return str.format("CREATE EDGE PublishedBy FROM (SELECT FROM Journal WHERE name='{0}') TO (SELECT FROM Paper WHERE paper_id='{1}')", journal_name, paper_id)

# Load JSON articles
def import_json_files():
    docs = read_files(FOLDER)
    paper_rids = []
    for doc in docs:
        paper = read_json(doc)

def import_csv_metadata():
    file_path = "/home/spark/Documents/repos/dl-covid19-kaggle-contest/Data/all_sources_metadata_2020-03-13_clean.csv"
    df = pd.read_csv(file_path)

    def _create_edges(index, row):
        paper_id = clean_str(row['sha'])

        if paper_id == None or len(paper_id) < 40:
            paper_id = str.format("na_paper_id_{0}", index)

        has_full_text = to_bool(row.has_full_text)
        journal_name = clean_str(row.journal)

        create_publishedby_edge(journal_name, paper_id)

        # list of authors is more complete in JSON files
        # only insert authors if there is no JSON file with full body text
        if not has_full_text:
            authors:List = authors_to_list(row.authors)
            for auth in authors:
                author_hash_id = hash_author(auth)               
                create_authoredby_edge(paper_id, author_hash_id)

    for i, row in df.iterrows():
        _create_edges(i, row)