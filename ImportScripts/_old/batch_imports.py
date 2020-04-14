import json
import os
import re
import hashlib
from pyorient import OrientDB, OrientRecord
from pyorient.exceptions import PyOrientCommandException
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
CSV_PATH = "/home/spark/Documents/repos/dl-covid19-kaggle-contest/Data/all_sources_metadata_2020-03-13_clean.csv"
HOST = "localhost"
PORT = 2424
DATABASE_NAME = "Covid19Dev"
DB_USER = "root"
DB_PWD = "spark123"
FOLDER = "/home/spark/Documents/repos/covid19kaggle/2020-03-13/"

socket = PySocket(HOST, PORT)
socket.connect()
client = OrientDB(socket)
client.db_open(DATABASE_NAME, DB_USER, DB_PWD)

# Open DB connection
def connect_db():
    socket = PySocket(HOST, PORT)
    socket.connect()
    client = OrientDB(socket)
    client.db_open(DATABASE_NAME, DB_USER, DB_PWD)
    return client

unique_institutions:List = []
unique_authors:List = []
unique_journal:List = []
unique_papers:Dict = {}
commands = []

batch_size = 25
batch_info = {
    'batch_size': batch_size,
    'commands': []
}

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

def trim(s) -> str:
    return re.sub(r'(^\s+|\s+$)', '', str(s))

def is_empty(s) -> bool:
    return s == None or s == 'NULL' or trim(s) == '' 

def clean_str(s:str) -> str:
    if s == None or str(s) == 'nan':
        return None

    s = re.sub( r'\n', ' ', str(s), re.MULTILINE)
    s = trim( re.sub(r'[^a-zA-Z0-9\s.-_#:,\']', '', str(s), re.MULTILINE))
    s = re.sub( r'(^\'+|\'+$)', "", s, re.MULTILINE)
    s = re.sub( r'\\+', "", s, re.DOTALL|re.MULTILINE)
    s = re.sub( r'\'+', "", s, re.DOTALL|re.MULTILINE)
    return None if len(s) == 0 else s

def to_int(s:str) -> int:
    try:
        n = int(is_dbnull(s))
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

def get_version(record: OrientRecord) -> str:
    if is_iter(record):
        return get_version(record[0])

    return record._version

def is_dbnull(s:str) -> str:
    if s == None:
        return 'NULL'

    return 'NULL' if clean_str(s) == None else str.format("'{0}'", clean_str(s))

def execute_batch(sql:str):
    commands = batch_info['commands']
    commands.append(sql)

    if len(commands) < 500:
        return

    # execute batch
    print("Executing batch")

    batch_cmds = ['begin']
    batch_cmds.extend(commands)
    batch_cmds.append('commit retry 100')
    cmd = ';'.join(batch_cmds)

    results = client.batch(cmd)
    print(results)

    # try:
    #     results = client.batch(cmd)
    #     print(results)
    #     print(str.format("Executed {0} commands", len(commands)))
    # except PyOrientCommandException as ex:
    #     print(ex)

    commands.clear()
    commands = []
    return

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
                "first": trim(names[1]),
                "last": trim(names[0])
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

def insert_institution(affiliation:Dict) -> str:
    if 'laboratory' not in affiliation and 'institution' not in affiliation:
        return None

    laboratory = clean_str(affiliation['laboratory'])
    institution = clean_str(affiliation['institution'])

    if is_empty(laboratory) and is_empty(institution):
        return None

    hash_id = hash_strings([institution, laboratory])
    
    ix = [i for i, j in enumerate(unique_institutions) if j == hash_id]
    if ix and len(ix) > 0:
        return None

    unique_institutions.append(hash_id)
    addrLine:str = None
    postCode:str = None
    region:str = None
    country:str = None

    if 'location' in affiliation:
        loc = affiliation['location']
        addrLine = is_dbnull(loc['addrLine']) if 'addrLine' in loc else 'NULL'
        postCode = is_dbnull(loc['postCode']) if 'postCode' in loc else 'NULL'
        region = is_dbnull(loc['region']) if 'region' in loc else 'NULL'
        country = is_dbnull(loc['country']) if 'country' in loc else 'NULL'

    sql = str.format("CREATE VERTEX Institution SET hash_id={0}, institution={1}, laboratory={2}, addrLine={3}, postCode={4}, region={5}, country={6}", \
        is_dbnull(hash_id), is_dbnull(institution), is_dbnull(laboratory), addrLine, postCode, region, country)

    execute_batch(sql)
    print(sql)
    return sql

def insert_journal(name:str, issn:str) -> str:
    journal_name = clean_str(name)
    journal_issn = is_dbnull(issn)

    if journal_name == None:
        return

    ix = [i for i, j in enumerate(unique_journal) if j == journal_name]
    if ix and len(ix) > 0:
        return None
        
    unique_journal.append(name)
    sql = str.format("CREATE VERTEX Journal SET name='{0}', issn={1}", journal_name, journal_issn)
    execute_batch(sql)
    print(sql)
    return sql

def insert_author(auth:Dict) -> str:
    hash_id = hash_author(auth)

    ix = [i for i, j in enumerate(unique_authors) if j == hash_id]
    if ix and len(ix) > 0:
        return None

    unique_authors.append(hash_id)
    first: str = is_dbnull(auth['first']) if 'first' in auth else 'NULL'  
    last: str = is_dbnull(auth['last']) if 'last' in auth else 'NULL'
    suffix: str = is_dbnull(auth['suffix']) if 'suffix' in auth else 'NULL'
    email: str = is_dbnull(auth['email']) if 'email' in auth else 'NULL'   
    middle: str = 'NULL'

    if 'middle' in auth and len(auth['middle']) > 0:
        middle = is_dbnull( ".".join( list( map(trim, auth['middle']) ) ) )

    sql =  str.format("CREATE VERTEX Author SET hash_id='{0}', first={1}, last={2}, middle={3}, suffix={4}, email={5}", \
        hash_id, first, last, middle, suffix, email)   
    execute_batch(sql)
    print(sql)
    return sql

def create_affiliation_edge(institution_hash:str, author_hash:str):
    sql = str.format("CREATE EDGE Affiliation FROM (SELECT FROM Institution WHERE institution_hash='{0}') TO (SELECT FROM Author WHERE hash_id='{1}')", institution_hash, author_hash)
    print(sql)
    execute_batch(sql)
    
def create_citation_edges(paper_id:str, bib:Dict):

    def _create(paper_id:str, author_hash:str) -> str:      
        return str.format("CREATE EDGE Citation FROM (SELECT FROM Paper WHERE paper_id='{0}') TO (SELECT FROM Author WHERE hash_id='{1}')", paper_id, author_hash)

    for author in bib['authors']:
        author_hash = hash_author(author)
        sql = _create(paper_id, author_hash)
        print(sql)
        execute_batch(sql)

    
def create_authoredby_edge(paper_id:str, author_hash_id:str) -> str:
    sql = str.format("CREATE EDGE AuthoredBy FROM (SELECT FROM Paper WHERE paper_id='{0}') TO (SELECT FROM Author WHERE hash_id='{1}')", paper_id, author_hash_id)
    print(sql)
    execute_batch(sql)

def create_publishedby_edge(journal_name:str, paper_id:str):
    sql = str.format("CREATE EDGE PublishedBy FROM (SELECT FROM Journal WHERE name='{0}') TO (SELECT FROM Paper WHERE paper_id='{1}')", journal_name, paper_id)
    print(sql)
    execute_batch(sql)

def create_edges(file_path):
    df = pd.read_csv(file_path)

    def _create_edges(index, row):
        paper_id = is_dbnull(row['sha'])

        if paper_id == None or len(paper_id) < 40:
            paper_id = str.format("na_paper_id_{0}", index)

        has_full_text = to_bool(row.has_full_text)
        journal_name = is_dbnull(row.journal)

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

def insert_paper(index:int, row:Dict, json_paper:Dict=None):

    def _is_correction(title:str) -> bool:
        # update paper if title starts with "Correction:..."
        rx_corrected = re.match("^correction:", str(title).lower())
        return rx_corrected and rx_corrected.group() in ['correction:']

    paper_id:str = clean_str(row['sha'])
    if paper_id == None or len(str(paper_id)) < 40:
        paper_id = str.format("na_paper_id_{0}", index)

    title = clean_str(row['title'])

    # don't import retracted papers
    try:
        rx_retracted = re.match("^retracted:", str(title).lower())
        if rx_retracted and rx_retracted.group() in ['retracted:']:
            return None
    except:
        pass

    # don't update if the corrected paper is already in the database
    try:
        ix = [i for i, j in enumerate(unique_papers) if j == paper_id]
        if ix and len(ix) > 0:
            if 'title' in unique_papers['paper_id']:
                paper_title = unique_papers['paper_id']['title']
                if _is_correction(paper_title) and not _is_correction(title):
                    return None
    except:
        pass

    try:
        unique_papers[paper_id] = {'title': title}
    except:
        pass

    title_short:str = None if title == None else title[0:50]
    abstract:str = clean_str( clean_str(row['abstract']) )
    doi = clean_str(row['doi'])
    source_x = clean_str(row['source_x'])
    mcid = clean_str(row['pmcid'])
    pubmed_id = clean_str(row['pubmed_id'])
    lic = clean_str(row['license'])   
    publish_time = clean_str(row['publish_time'])
    ms_paper_id = clean_str(row['Microsoft Academic Paper ID'])
    who_covidence = clean_str(row['WHO #Covidence'])
    pmcid = clean_str(row['pmcid'])
    full_text:str = None
    authors:str = clean_str( json.dumps( authors_to_list(row['authors']) ))
    
    if json_paper != None:
        metadata:Dict = json_paper['metadata']
        title = clean_str(metadata['title'])

        abstracts = []
        for ab in json_paper['abstract']:
            s = clean_str(ab['text'])
            if s != None:
                abstracts.append(s)

        if len(abstracts) > 0:
            abstract = " ".join(abstracts)

        # Combine all sections in body_text array
        body_text = []
        for section in json_paper['body_text']:
            s = clean_str(section['text'])
            if s != None:
                body_text.append(s)

        if len(body_text) > 0:
            full_text = " ".join(body_text)

        for author in metadata['authors']:
            insert_author(author)

            if 'affiliation' in author:
                insert_institution(author['affiliation'])

        for bibref in json_paper['bib_entries']:
            bib = json_paper['bib_entries'][bibref]
            insert_journal(bib['venue'], bib['issn'])

            for author in bib['authors']:
                insert_author(author)
    else:
        # list of authors is more complete in JSON files
        # only insert authors if there is no JSON file with full body text      
        for auth in authors:
            insert_author(auth)

    p = Paper()
    p.paper_id = paper_id 
    p.title = title
    p.title_short = title_short
    p.abstract = abstract
    p.body_text = full_text
    p.doi = doi
    p.source_x = source_x
    p.mcid = mcid
    p.pubmed_id = pubmed_id
    p.has_full_text = (0 if full_text == None else 1)
    p.license = lic
    p.ms_paper_id = ms_paper_id
    p.pmcid = pmcid
    p.publish_time = publish_time
    p.who_covidence = who_covidence
    p.authors = authors

    vertex = {
        "@Paper": p.__dict__
    }

    record:OrientRecord = client.record_create(22, vertex)
    print(record._rid)
    #sql = str.format("CREATE VERTEX Paper SET paper_id='{0}', title={1}, title_short={2}, abstract={3}, body_text={4}, doi={5}, source_x={6}, mcid={7}, pubmed_id={8}, license={9}, publish_time={10}, ms_paper_id={11}, who_covidence={12}, has_full_text={13}, authors={14}", \
        #paper_id,title,title_short,abstract,full_text,doi,source_x,mcid,pubmed_id,lic,publish_time,ms_paper_id,who_covidence, (0 if full_text == None else 1), authors)
    
    return None

# Load JSON articles
def get_json_papers():
    papers = []

    for root, folders, docs in os.walk(FOLDER):
        for doc in docs:
            if '.json' not in doc:
                continue

            papers.append( os.path.join(root, doc) )
   
    return papers

def insert_vertices():
    def _get_paper_id(path:str) -> str:
        rx = re.search(r'[\w\d]{40}.json$', str(path).lower())
        if rx:
            return rx.group().replace('.json', '')

        return None

    df = pd.read_csv(CSV_PATH)
    json_papers = get_json_papers()
    json_ids = [_get_paper_id(path) for path in json_papers]

    for index, row in df.iterrows():
        paper_id = str(row['sha'])
        if paper_id != 'nan':
            ix = [i for i, j in enumerate(json_ids) if j == paper_id]
            if ix and len(ix) > 0:
                json_paper = read_json(json_papers[ix[0]])
                insert_paper(index, row, json_paper)
        else:
            insert_paper(index, row)


insert_vertices()
client.close()