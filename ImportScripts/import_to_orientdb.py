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
from covid19_classes import Paper

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
DATABASE_NAME = "Covid19"
DB_USER = "admin"
DB_PWD = "admin"
PAPER_CLUSTER = 21
BIB_ENTRY_CLUSTER = 26
AUTHOR_CLUSTER = 25
AUTHOR_BIB_ENTRY_CLUSTER = 24
PAPER_AUTHOR_CLUSTER = 22
PAPER_BIB_ENTRY_CLUSTER = 23
AFFILIATION_CLUSTER = 27
AUTHOR_AFFILIATION_CLUSTER = 28
FOLDER = "/home/spark/Documents/repos/covid19kaggle/2020-03-13/"

# Open DB connection
socket = PySocket(HOST, PORT)
socket.connect()
client = OrientDB(socket)
client.db_open(DATABASE_NAME, DB_USER, DB_PWD) # change to your database name



def to_bool(s):
    rx = re.match("^(1|true|yes)$", trim(str(s).lower()))
    if rx:
        return rx.group() in ['1', 'yes', 'true']

    return False
    
def is_rid(rid:str) -> bool:
    rx = re.match("^#\d+:\d+$", rid)
    if rx:
        return rx.group() == rid 

    return False

def trim(s) -> str:
    return re.sub("(^s\+|\s+$)", "", str(s))

def is_empty(s) -> bool:
    return s == None or s == 'NULL' or trim(s) == '' 

def clean_str(s:str) -> str:
    if s == None:
        return s

    if str(s) == 'nan':
        return None

    return trim(str(s)) if not is_empty(str(s)) else None 

def hash_author(first:str, last:str, middle:str=None, suffix:str=None, email:str=None) -> str:
    f = '' if is_empty(first) else trim(first) 
    l = '' if is_empty(last) else trim(last)
    m = '' if is_empty(middle) else trim(middle)
    s = '' if is_empty(suffix) else trim(suffix)
    e = '' if is_empty(email) else trim(email)

    combined = str.format("{0}{1}{2}{3}{4}", f, l, m, s, e)
    hashed = hashlib.md5(combined.encode())
    return hashed.hexdigest()

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
    return str(record.__dict__['_OrientRecord__rid'])

def create_paper_author_edge(paper_rid:str, author_rid:str) -> OrientRecord:
    if is_rid(paper_rid) and is_rid(author_rid):
        # edges = client.query(str.format("SELECT FROM AuthorPaper WHERE IN = {0} AND OUT = {1}", author_rid, paper_rid))
        # if len(edges) > 0:
        #     return edges[0]

        edge_sql = str.format("CREATE EDGE AuthorPaper FROM {0} TO {1}", author_rid, paper_rid)
        return client.command(edge_sql)

    return None

def create_paper_bib_edge(paper_rid:str, bib_rid:str) -> OrientRecord:
    if is_rid(paper_rid) and is_rid(bib_rid):
        # edges = client.query(str.format("SELECT FROM BibEntryPaper WHERE IN = {0} AND OUT = {1}", bib_rid, paper_rid))
        # if len(edges) > 0:
        #     return edges[0]

        edge_sql = str.format("CREATE EDGE BibEntryPaper FROM {0} TO {1}", bib_rid, paper_rid)
        return client.command(edge_sql)

    return None

def create_author_bib_edge(bib_rid:str, author_rid:str) -> OrientRecord:
    if is_rid(author_rid) and is_rid(bib_rid):
        # edges = client.query(str.format("SELECT FROM AuthorBibEntry WHERE IN = {0} AND OUT = {1}", author_rid, bib_rid))
        # if len(edges) > 0:
        #     return edges[0]

        edge_sql = str.format("CREATE EDGE AuthorBibEntry FROM {0} TO {1}", bib_rid, author_rid)
        return client.command(edge_sql)

    return None

def create_author_affiliation_edge(affiliation_rid:str, author_rid:str) -> OrientRecord:
    if is_rid(author_rid) and is_rid(affiliation_rid):
        edge_sql = str.format("CREATE EDGE AuthorAffiliation FROM {0} TO {1}", author_rid, affiliation_rid)
        return client.command(edge_sql)

    return None

def insert_affiliation(author_rid:str, affiliation:Dict) -> str: 

    if 'laboratory' not in affiliation and 'institution' not in affiliation:
        return None

    if is_empty(affiliation['laboratory']) and is_empty(affiliation['institution']):
        return None

    record: OrientRecord = None

    lab:str = trim(affiliation['laboratory']) if not is_empty(affiliation['laboratory']) else ''

    inst:str = trim(affiliation['institution']) if not is_empty(affiliation['institution']) else ''

    postCode:str = None 
    settlement:str = None
    region:str = None
    country:str = None

    if 'location' in affiliation:
        location = affiliation['location']
        postCode = trim(location['postCode']) if 'postCode' in location else None
        settlement= trim(location['settlement']) if 'settlement' in location else None
        region = trim(location['region']) if 'region' in location else None
        country = trim(location['country']) if 'country' in location else None

    hash_id = hashlib.md5( str.format("{0}{1}", inst, lab).encode() ).hexdigest()

    affiliations: List = client.query(str.format("select * from Affiliation where hash_id = '{0}'", hash_id))

    if len(affiliations) > 0:
        record = affiliations[0]
    else:
        record = client.record_create(AFFILIATION_CLUSTER ,{
            "@Affiliation": {
                "laboratory": lab if not is_empty(lab) else None,
                "institution": inst if not is_empty(inst) else None,
                "postCode": postCode,
                "settlement": settlement,
                "region": region,
                "country": country,
                "hash_id": hash_id
            }
        })

    affiliation_rid:str = get_rid(record)
    create_author_affiliation_edge(author_rid, affiliation_rid)

    return affiliation_rid

def insert_author(auth:Dict) -> str:
    
    first: str = trim(auth['first']) if ('first' in auth and not is_empty(auth['first'])) else None
    
    last: str = trim(auth['last']) if ('last' in auth and not is_empty(auth['last'])) else None

    suffix: str = trim(auth['suffix']) if ('suffix' in auth and not is_empty(auth['suffix'])) else None

    email: str = trim(auth['email']) if ('email' in auth and not is_empty(auth['email'])) else None
    
    middle: str = None
    if 'middle' in auth and len(auth['middle']) > 0:
        middle = ".".join( list( map(trim, auth['middle']) ) )

    hash_id = hash_author(first, last, middle, suffix, email)
    
    # Check if author already exists, and insert if not.
    authors: List = client.query(str.format("select * from Author where hash_id = '{0}'", hash_id))
    
    record:OrientRecord = None

    if len(authors) > 0:
        record = authors[0]
    else:
        vertex = {
            "@Author": {
                "first": first,
                "middle": middle,
                "last": last,
                "email": email,
                "suffix": suffix,
                "hash_id": hash_id
            }
        }
        record = client.record_create(AUTHOR_CLUSTER, vertex)

    author_rid = get_rid(record)

    if 'affiliation' in auth:
        insert_affiliation(author_rid, auth['affiliation'])

    return author_rid
    # /def insert_author:

def insert_bib_entry(paper_id:str, bib:Dict) -> str:

    ref_id = bib['ref_id']
    vertex = {
        "@BibEntry": {
            "ref_id": bib['ref_id'],
            "paper_id": paper_id,
            "title": bib['title'],
            "year": bib['year'],
            "venue": bib['venue'],
            "issn": bib['issn']
        }
    }

    bib_rid:str = None
    record: OrientRecord = client.record_create(BIB_ENTRY_CLUSTER, vertex)
    bib_rid = get_rid(record)

    #bib authors
    if 'authors' in bib:
        authors = bib['authors']
        for auth in authors:
            author_rid = insert_author(auth)
            bib_edge = create_author_bib_edge(author_rid, bib_rid)

    return bib_rid

def insert_paper(data) -> str:
    paper_id:str = data['paper_id']
    metadata:str = data['metadata']  
    title:str = metadata['title']
    title_short:str = title[0:50]
    authors: List = metadata['authors']
    bib_entries: List = data['bib_entries']
    paper_rid:str = None

    abstracts = []
    for ab in data['abstract']:
        abstracts.append(ab['text'])

    abstract = " ".join(abstracts)

    # Combine all sections in body_text array
    body_text = []
    for section in data['body_text']:
        body_text.append(section['text'])

    full_text = " ".join(body_text)

    paper = Paper(paper_id)
    paper.title = title
    paper.abstract = abstract
    paper.body_text = full_text
    paper.title_short = title_short

    vertex = {
        "@Paper": paper.__dict__
    }

    paper_rid:str = None
    record: OrientRecord = None

    papers = client.query(str.format("select * from Paper where paper_id = '{0}'", paper_id))
    # update
    if papers != None and len(papers) > 0:
        record = papers[0]
        paper_rid = record._rid
        version = record._version
        client.record_update(paper_rid, paper_rid, vertex, version)
    # insert
    else:
        record = client.record_create(PAPER_CLUSTER, vertex)
        paper_rid = get_rid(record)

    # authors
    for auth in authors:      
        author_rid:str = insert_author(auth)
        create_paper_author_edge(paper_rid, author_rid)
        
    # bib entries
    for bibs in bib_entries:
        bib = bib_entries[bibs]
        bib_rid = insert_bib_entry(paper_id, bib)
        # create edge between paper and bib entry
        create_paper_bib_edge(paper_rid, bib_rid)

    return paper_rid
    # def

# TEST
def unit_test():
    test_paper = read_json(FOLDER+"biorxiv_medrxiv/biorxiv_medrxiv/00d16927588fb04d4be0e6b269fc02f0d3c2aa7b.json")
    paper_rid = insert_paper(test_paper)
    print(paper_rid)
    
    #client.record_delete(PAPER_CLUSTER, test_paper_id)

# unit_test()

# Load JSON articles
def import_json_files():
    docs = read_files(FOLDER)
    paper_rids = []
    for doc in docs:
        paper = read_json(doc)
        paper_rid = insert_paper(paper)
        paper_rids.append(paper_rid)
        print(paper_rid)

    print("Imported", len(paper_rids), "documents.")

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

def insert_csv_paper_model(index, row):

    def _insert(vertex):
        record = client.record_create(PAPER_CLUSTER, vertex)  
        return get_rid(record)

    def _is_correction(title:str) -> bool:
        # update paper if title starts with "Correction:..."
        rx_corrected = re.match("^correction:", str(title).lower())
        return rx_corrected and rx_corrected.group() in ['correction:']

    paper_id:str = str(row['sha'])
    if paper_id == None or len(paper_id) < 40:
        paper_id = str.format("na_paper_id_{0}", index)

    title = clean_str(row.title)

    # don't import retracted papers
    rx_retracted = re.match("^retracted:", str(title).lower())
    if rx_retracted and rx_retracted.group() in ['retracted:']:
        return None

    paper: Paper = Paper(paper_id)
    paper.title = title
    paper.doi = clean_str(row.doi)
    paper.source_x = clean_str(row.source_x)
    paper.pmcid = clean_str(row.pmcid)
    paper.pubmed_id = clean_str(row.pubmed_id)
    paper.license = clean_str(row.license)
    paper.abstract = clean_str(row.abstract)
    paper.publish_time = clean_str(row.publish_time)
    paper.journal = clean_str(row.journal)
    paper.ms_paper_id = clean_str(row['Microsoft Academic Paper ID'])
    paper.who_covidence = clean_str(row['WHO #Covidence'])
    paper.has_full_text = to_bool(row.has_full_text)
    authors:List = authors_to_list(row.authors)

    vertex = {
        "@Paper": paper.__dict__
    }

    records = client.query(str.format("select * from Paper where paper_id = '{0}'", paper_id))

    # update
    if records != None and len(records) > 0:
        record: OrientRecord = records[0]
        paper_rid = record._rid
        version = record._version
        # don't update if the corrected paper is already in the database
        if _is_correction(record.title) and not _is_correction(paper.title):
            return record._rid
        else:        
            success = client.record_update(paper_rid, paper_rid, vertex, version)
            return paper_rid
    
    # insert
    paper_rid = _insert(vertex)

    for auth in authors:
        author_rid = insert_author(auth)
        create_paper_author_edge(paper_rid, author_rid)

    return paper_rid

def import_csv_metadata():
    file_path = "/home/spark/Documents/repos/dl-covid19-kaggle-contest/Data/all_sources_metadata_2020-03-13_clean.csv"
    df = pd.read_csv(file_path)
    for index, row in df.iterrows():
        paper_rid = insert_csv_paper_model(index, row)
        print(paper_rid)

# step 1
#import_csv_metadata()

# step 2 - update papers with body text from JSON files, etc.
import_json_files()

client.close()