import json
import os
import pyorient
import pyorient.ogm


"""
Import JSON articles into OrientDB (WIP)
John Bonfardeci
2020-03-26

Run in Python 3.7.3 64-bit env

PyOrient docs - https://orientdb.com/docs/3.0.x/pyorient/PyOrient.html
"""

# change to root folder on your system
dir = "/home/spark/Documents/repos/covid19kaggle/2020-03-13/"

client = "" # change to your instance address and port
db = "" # change to your database name
articles = "" # change to your collection name

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

def execute_query(q):
    # TODO
    id = None
    return id 

def upsert_author(auth):
    middle = 'NULL'
    if len(auth['middle']) > 0:
        middle = ".".join(auth['middle'])

    email = 'NULL'
    if email in auth:
        email = auth['email']

    # TODO - check if author already exists

    q = str.format("insert into Authors(first, middle, last, suffix, email) values('{0}', '{1}', '{2}', '{3}')"
                    , auth['first']
                    , middle
                    , auth['last']
                    , email)

    return execute_query(q)

def insert_bib_entry(paper_id, bib):
    q = str.format("insert into BibEntries(ref_id, paper_id, title, year, venue, issn) values('{0}', '{1}', '{2}', '{3}'. '{4}', '{5}')"
                    , bib['ref_id']
                    , paper_id
                    , bib['title']
                    , bib['year']
                    , bib['venue']
                    , bib['issn'])

    return execute_query(q) 
        
def insert_paper(data):
    metadata = data['metadata']
    paper_id = data['paper_id']
    title = metadata['title']
    authors = metadata['authors']
    bib_entries = data['bib_entries']

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

    # paper
    q = str.format("insert into Papers(paper_id, title, abstract, body_text) values('{0}', '{1}', '{2}', '{3}')"
                    , paper_id
                    , title
                    , abstract
                    , full_text)

    db_id = execute_query(q)
    
    # authors
    for auth in authors:      
        upsert_author(auth)

    for bibs in bib_entries:
        b = bib_entries[bibs]
        insert_bib_entry(paper_id, b)

    return db_id
    # def


#article = read_json(dir+"biorxiv_medrxiv/biorxiv_medrxiv/0a43046c154d0e521a6c425df215d90f3c62681e.json")
#print(article['metadata']['title'])

# Load JSON articles
docs = read_files(dir)
paper_ids = []

for doc in docs:
    try:
        paper = read_json(doc)
        paper_id = insert_paper(paper)
        paper_ids.append(paper_id)
    except:
        print(doc)

print("Imported", len(paper_ids), "documents.")