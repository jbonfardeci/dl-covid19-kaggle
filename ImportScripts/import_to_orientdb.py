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
AUTHOREDBY_CLUSTER = 26 # 'AuthoredByCluster'
PUBLISHEDBY_CLUSTER = 25 # 'PublishedByCluster'
AFFILIATION_CLUSTER = 27 # 'AffiliationCluster'
CITATION_CLUSTER = 28 # 'CitationCluster'

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

def to_int(s:str) -> int:
    try:
        n = int(clean_str(s))
        return n
    except:
        return None

def hash_author(first:str, last:str, middle:str=None, suffix:str=None, email:str=None) -> str:
    f = '' if is_empty(first) else trim(first) 
    l = '' if is_empty(last) else trim(last)
    m = '' if is_empty(middle) else trim(middle)
    s = '' if is_empty(suffix) else trim(suffix)
    e = '' if is_empty(email) else trim(email)

    combined = str.format("{0}{1}{2}{3}{4}", f, l, m, s, e)
    hashed = hashlib.md5(combined.encode())
    return hashed.hexdigest()

def hash_strings(strings:List) -> str:
    a = [trim(s) for s in strings if not is_empty(s)]
    return hashlib.md5(''.join(a).encode()).hexdigest()

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

def get_rid(record: OrientRecord) -> str:
    return str(record.__dict__['_OrientRecord__rid'])

def create_publishedby_edge(paper_rid:str, journal_rid:str) -> str:
    if not is_rid(paper_rid) or not is_rid(journal_rid):
        return None

    record:OrientRecord = client.query("SELECT * FROM PublishedBy WHERE FROM = {0} and TO = {1}", \
        paper_rid, journal_rid)

    if record and len(record) > 0:
        return record[0]._rid

    record = client.command(str.format("CREATE EDGE PublishedBy FROM {0} TO {1}", paper_rid, journal_rid))
    return record._rid

def create_authoredby_edge(author_rid:str, paper_rid:str) -> str:
    if not is_rid(author_rid) or not is_rid(paper_rid):
        return None

    #return None
    record: OrientRecord = client.query(str.format("SELECT * FROM AuthoredBy WHERE FROM = {0} and TO = {1}", \
        author_rid, paper_rid))

    if record and len(record) > 0:
        return record[0]._rid

    record = client.command(str.format("CREATE EDGE AuthoredBy FROM {0} TO {1}", paper_rid, author_rid))
    return get_rid(record)

def create_affiliation_edge(author_rid:str, institution_rid:str) -> str:
    if not is_rid(author_rid) or not is_rid(institution_rid):
        return None

    record: OrientRecord = client.query("SELECT * FROM Affiliation WHERE FROM = {0} and TO = {1}", \
        institution_rid, author_rid)

    if record and len(record) > 0:
        return record[0]._rid

    record = client.command(str.format("CREATE EDGE Affiliation FROM {0} TO {1}", author_rid, institution_rid))
    return record._rid

def insert_institution(affiliation:Dict) -> str:

    if 'laboratory' not in affiliation and 'institution' not in affiliation:
        return None

    laboratory = clean_str(affiliation['laboratory'])
    institution = clean_str(affiliation['institution'])

    if is_empty(laboratory) and is_empty(institution):
        return None

    hash_id = hash_strings([institution, laboratory])
    record: OrientRecord = client.query(str.format("SELECT * FROM Institution WHERE hash_id = '{0}'", hash_id))

    if record and len(record) > 0:
        return record[0]._rid
    
    o = Institution()
    o.hash_id = hash_id
    o.laboratory = laboratory
    o.institution_name = institution

    record = client.record_create(INSTITUTION_CLUSTER, {
        "@Institution": o.__dict__
    })

    return record._rid

def insert_author(auth:Dict) -> str:
    
    def _find(hash_id:str) -> str:
        record:OrientRecord = client.query(str.format("SELECT * FROM Author WHERE hash_id = '{0}'", hash_id))
    
        if record and len(record) > 0:
            return record[0]._rid

        return None

    def _create(hash_id, first, last, middle, suffix, email):
        o = Author()
        o.hash_id = hash_id
        o.first = first
        o.middle = middle
        o.last = last
        o.suffix = suffix
        o.email = email
        record = client.record_create(AUTHOR_CLUSTER, {
            "@Author": o.__dict__
        })
        return record._rid

    first: str = trim(auth['first']) if ('first' in auth and not is_empty(auth['first'])) else None  
    last: str = trim(auth['last']) if ('last' in auth and not is_empty(auth['last'])) else None
    suffix: str = trim(auth['suffix']) if ('suffix' in auth and not is_empty(auth['suffix'])) else None
    email: str = trim(auth['email']) if ('email' in auth and not is_empty(auth['email'])) else None   
    middle: str = None
    if 'middle' in auth and len(auth['middle']) > 0:
        middle = ".".join( list( map(trim, auth['middle']) ) )

    hash_id = hash_strings([first, last, middle, suffix, email])   
    author_rid:str = _find(hash_id)

    if author_rid == None:
        author_rid = _create(hash_id, first, last, middle, suffix, email)

    if 'affiliation' in auth:
        institution_rid = insert_institution(auth['affiliation'])
        create_affiliation_edge(author_rid, institution_rid)

    return author_rid
    # /def insert_author:

def create_citation_edges(paper_rid:str, bib:Dict) -> List:

    ref_id:str = clean_str(bib['ref_id'])
    journal_name = clean_str(bib['venue'])

    def _find_edge(author_rid:str) -> str:
        record:OrientRecord = client.query("SELECT * FROM Citation WHERE ref_id = '{0}' AND FROM = {1} AND TO = {2}", \
            ref_id, paper_rid, author_rid)

        if record and len(record) > 0:
            return record[0]._rid

        return None

    def _create(author_rid:str) -> str:      
        title = clean_str(bib['title']),
        year = to_int(bib['year'])
        issn = clean_str(bib['issn'])
        record = client.command(str.format("CREATE EDGE Citation FROM {0} TO {1} SET ref_id = '{2}', title = '{3}', year = {4}, issn = '{5}'", \
            paper_rid, author_rid, ref_id, title, year, issn))
        return record._rid

    rids = []

    for author in bib['authors']:
        author_rid:str = insert_author(author)
        citation_rid = _find_edge(author_rid)
        if citation_rid == None:
            rids.append( _create(author_rid) )
        else:
            continue

    return rids
    
def insert_paper(data) -> str:
    paper_id:str = clean_str(data['paper_id'])
    metadata:Dict = data['metadata']  
    title:str = clean_str(metadata['title'])
    title_short:str = title[0:50]
    bib_entries:List = data['bib_entries']
    paper_rid:str = None
    record: OrientRecord = None

    abstracts = []
    for ab in data['abstract']:
        abstracts.append(ab['text'])

    abstract = " ".join(abstracts)

    # Combine all sections in body_text array
    body_text = []
    for section in data['body_text']:
        body_text.append(section['text'])

    full_text = " ".join(body_text)

    paper:Paper = Paper()
    paper.paper_id = paper_id
    paper.title = title
    paper.abstract = abstract
    paper.body_text = full_text
    paper.title_short = title_short

    vertex = {
        "@Paper": paper.__dict__
    }

    papers = client.query(str.format("SELECT * FROM Paper WHERE paper_id = '{0}'", paper_id))
    # update
    if papers and len(papers) > 0:
        record = papers[0]
        paper_rid = record._rid
        version = record._version
        client.record_update(paper_rid, paper_rid, vertex, version)
    # insert
    else:
        record = client.record_create(PAPER_CLUSTER, vertex)
        paper_rid = get_rid(record)

    # authors
    paper_authors: List = metadata['authors']
    for auth in paper_authors:      
        author_rid:str = insert_author(auth)
        create_authoredby_edge(author_rid, paper_rid)
        
    # bib entries (citations)
    for entry in bib_entries: 
        create_citation_edges(paper_rid, bib_entries[entry])

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

def insert_journal(name:str) -> str:
    name = clean_str(name)

    if name == None:
        return None

    name = name.replace("'", "")
    name = name.replace("\\", "")
    record: OrientRecord = client.query(str.format("SELECT * FROM Journal WHERE name = '{0}'", name))

    if record and len(record) > 0:
        return record[0]._rid

    vertex = {
        "@Journal": {
            "name": name
        }
    }

    record = client.record_create(JOURNAL_CLUSTER, vertex)
    return record._rid

def insert_csv_paper_model(index, row):

    def _insert(vertex):
        record: OrientRecord = client.record_create(PAPER_CLUSTER, vertex)  
        return record._rid

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

    paper:Paper = Paper()
    paper.paper_id = paper_id
    paper.title = title
    paper.title_short = title[0:50]
    paper.doi = clean_str(row.doi)
    paper.source_x = clean_str(row.source_x)
    paper.pmcid = clean_str(row.pmcid)
    paper.pubmed_id = clean_str(row.pubmed_id)
    paper.license = clean_str(row.license)
    paper.abstract = clean_str(row.abstract)
    paper.publish_time = clean_str(row.publish_time)
    paper.ms_paper_id = clean_str(row['Microsoft Academic Paper ID'])
    paper.who_covidence = clean_str(row['WHO #Covidence'])
    paper.has_full_text = to_bool(row.has_full_text)

    vertex = {
        "@Paper": paper.__dict__
    }

    records = client.query(str.format("SELECT * FROM Paper WHERE paper_id = '{0}'", paper_id))

    # update
    if records and len(records) > 0:
        record: OrientRecord = records[0]
        paper_rid = record._rid
        version = record._version
        # don't update if the corrected paper is already in the database
        if _is_correction(record.title) and not _is_correction(paper.title):
            return record._rid
        else:        
            record = client.record_update(paper_rid, paper_rid, vertex, version)
            return record._rid
    
    # insert
    paper_rid = _insert(vertex)

    # insert journal
    journal = clean_str(row.journal)
    if journal != None:
        journal_rid = insert_journal(journal)
        create_publishedby_edge(paper_id, journal_rid)

    # list of authors is more complete in JSON files
    # only insert authors if there is no JSON file with full body text
    if not paper.has_full_text:
        authors:List = authors_to_list(row.authors)
        for auth in authors:
            author_rid = insert_author(auth)
            print(author_rid)
            if is_rid(author_rid):
                create_authoredby_edge(author_rid, paper_rid)

    return paper_rid

def import_csv_metadata():
    file_path = "/home/spark/Documents/repos/dl-covid19-kaggle-contest/Data/all_sources_metadata_2020-03-13_clean.csv"
    df = pd.read_csv(file_path)
    for index, row in df.iterrows():
        paper_rid = insert_csv_paper_model(index, row)
        print(paper_rid)

# step 1
import_csv_metadata()

# step 2 - update papers with body text from JSON files, etc.
#import_json_files()

client.close()