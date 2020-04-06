import json
import os
import re
import hashlib
import pyodbc 

"""
Import JSON articles into SQL Server
John Bonfardeci
2020-04-05
"""

# change to your params

ROOT = "C:\\Users\\bonfardeci-j\\source\\covid19_kaggle\\"
FOLDER = ROOT+"json\\"
TARGET = ROOT+"csv\\"

batch_info = {
    'commands': [],
    'paper_count': 0
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

def trim(s):
    return re.sub(r'(^\s+|\s+$)', '', str(s))

def is_empty(s) -> bool:
    return s == None or s == 'NULL' or trim(s) == '' 

def clean_str(s):
    if s == None or str(s) == 'nan':
        return None

    s = re.sub( r'\n', ' ', str(s), re.DOTALL)
    s = re.sub( r'\r\n', ' ', s, re.DOTALL)
    #s = re.sub( r'[^a-zA-Z0-9\s\.\-_\#\:\,]', '', s, re.DOTALL)
    s = re.sub( r'(^\'+|\'+$)', "", s, re.DOTALL)
    s = re.sub( r'\\+', "", s, re.DOTALL)
    s = re.sub( r'\'+', '\'\'', s, re.DOTALL)
    s = s.encode('ascii', 'ignore').decode()
    return None if len(s) == 0 else s

def to_int(s) -> int:
    try:
        n = int(is_dbnull(s))
        return n
    except:
        return None

def hash_author(author):

    def _in(prop, o):
        return trim(o[prop]) if prop in o else ''

    f = _in('first', author)
    l = _in('last', author)
    m = _in('middle', author)
    s = _in('suffix', author)
    e = _in('email', author)

    combined = str.format("{0}{1}{2}{3}{4}", f, l, m, s, e)
    hashed = hashlib.md5(combined.encode())
    return hashed.hexdigest()

def hash_strings(strings):
    a = [trim(s) for s in strings if not is_empty(s)]
    return hashlib.md5(''.join(a).encode()).hexdigest()

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

def is_dbnull(s):
    if s == None:
        return 'NULL'

    return 'NULL' if clean_str(s) == None else str.format("'{0}'", clean_str(s))

def execute_batch(sql):
    commands = batch_info['commands']
    commands.append(sql)
    
    if len(commands) < 100:
        return
        
    print('Executing batch...')
    batch = ';\r\n'.join(commands)

    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=ZBOOK27\MSSQLSERVER17;'
                          'Database=covid19;'
                          'Trusted_Connection=yes;')
    
    cursor = conn.cursor()
    try:
        cursor.execute(batch)
        conn.commit()
    except:
        with open(ROOT+"sql_log.sql", "w") as f:
            f.writelines(batch)
            
        raise Exception("SQL syntax error. Exiting.")
        
    print('Batch executed.')
    print(str.format("Papers imported {0}", batch_info['paper_count']))
    commands.clear()
    
def insert_institution(affiliation):
    if 'laboratory' not in affiliation and 'institution' not in affiliation:
        return None

    laboratory = clean_str(affiliation['laboratory'])
    institution = clean_str(affiliation['institution'])

    if laboratory == None and institution == None:
        return None

    hash_id = hash_strings([institution, laboratory])
    addrLine = None
    postCode = None
    region = None
    country = None

    if 'location' in affiliation:
        loc = affiliation['location']
        addrLine = loc['addrLine'] if 'addrLine' in loc else None
        postCode = loc['postCode'] if 'postCode' in loc else None
        region = loc['region'] if 'region' in loc else None
        country = loc['country'] if 'country' in loc else None
    
    inst = {
        'hash_id': hash_id, 
        'institution_name': institution, 
        'laboratory': laboratory, 
        'addrLine': addrLine, 
        'postCode': postCode, 
        'region': region, 
        'country': country
    }
    
    o =  json.loads(json.dumps(inst), encoding='utf-8')
    
    s = """INSERT INTO import.Institution(hash_id, institution_name, laboratory, addrLine, 
            postCode, region, country) VALUES({0}, {1}, {2}, {3}, {4}, {5}, {6})"""
    
    sql = str.format(s, is_dbnull(o['hash_id']), is_dbnull(o['institution_name']), is_dbnull(o['laboratory']), \
            is_dbnull(o['addrLine']), is_dbnull(o['postCode']), is_dbnull(o['region']), is_dbnull(o['country']))
    
    execute_batch(sql)

    return hash_id

def insert_journal(name, issn):
    journal_name = clean_str(name)
    journal_issn = clean_str(issn)

    if journal_name == None and journal_issn == None:
        return

    hash_id = hash_strings([journal_name, journal_issn])
    
    journal = {
        'hash_id': hash_id, 
        'journal_name': journal_name, 
        'issn': journal_issn
    }
    
    o = json.loads(json.dumps(journal), encoding='utf-8')
    
    sql = str.format("INSERT INTO import.Journal(hash_id, journal_name, issn) VALUES({0}, {1}, {2})", \
        is_dbnull(o['hash_id']), is_dbnull(o['journal_name']), is_dbnull(o['issn']))
    
    execute_batch(sql)
   
    return hash_id

def insert_author(auth):
    hash_id = hash_author(auth)
    first = clean_str(auth['first']) if 'first' in auth else None  
    last = clean_str(auth['last']) if 'last' in auth else None
    suffix = clean_str(auth['suffix']) if 'suffix' in auth else None
    email = clean_str(auth['email']) if 'email' in auth else None  
    middle = None

    if 'middle' in auth and len(auth['middle']) > 0:
        middle = clean_str( ".".join( list( map(trim, auth['middle']) ) ) )
        
    author = {
        'hash_id': hash_id,
        'first_name': first,
        'last_name': last,
        'middle': middle,
        'suffix': suffix,
        'email': email
    }
    
    o = json.loads(json.dumps(author), encoding='utf-8')
    
    s = """INSERT INTO import.Author(hash_id,first_name,last_name,middle,suffix,email) 
            VALUES({0}, {1}, {2}, {3}, {4}, {5})"""
    sql =  str.format(s, is_dbnull(o['hash_id']), is_dbnull(o['first_name']), is_dbnull(o['last_name']), is_dbnull(o['middle']), \
                      is_dbnull(o['suffix']), is_dbnull(o['email']))   
    
    execute_batch(sql)
    
    return hash_id

def insert_affiliation(institution_hash, author_hash):
    if institution_hash == None or author_hash == None:
        return 

    sql = str.format("INSERT INTO import.Affiliation(institution_hash, author_hash) VALUES('{0}', '{1}')", \
                     institution_hash, author_hash) 
    
    execute_batch(sql)
    
def insert_citation(author_hash, paper_id):
    if paper_id == None:
        return 

    sql = str.format("INSERT INTO import.Citation(author_hash, paper_id) VALUES('{0}', '{1}')", author_hash, paper_id)
    
    execute_batch(sql)
    
def insert_authored(paper_id, author_hash):
    if paper_id == None or author_hash == None:
        return

    sql = str.format("INSERT INTO import.Authored(author_hash, paper_id) VALUES('{0}', '{1}')", author_hash, paper_id)
    
    execute_batch(sql)

def insert_publishedby(journal_hash, paper_id):
    if journal_hash == None or paper_id == None:
        return
        
    sql = str.format("INSERT INTO import.PublishedBy(journal_hash, paper_id) VALUES('{0}', '{1}')", \
                     journal_hash, paper_id)
    
    execute_batch(sql)
    
def insert_paper(json_paper):
    paper_id = json_paper['paper_id']
    metadata = json_paper['metadata']
    authors = metadata['authors']
    bib_entries = json_paper['bib_entries']
    title = clean_str(metadata['title'])
    body_text = None
    abstract = None
    abstract_nodes = []
    text_nodes = []

    # Combine all sections in abstract array
    for ab in json_paper['abstract']:
        s = clean_str(ab['text'])
        if s != None:
            abstract_nodes.append(s)

    if len(abstract_nodes) > 0:
        abstract = " ".join(abstract_nodes)

    # Combine all sections in body_text array    
    for section in json_paper['body_text']:
        s = clean_str(section['text'])
        if s != None:
            text_nodes.append(s)

    if len(text_nodes) > 0:
        body_text = " ".join(text_nodes)
        
    paper = {
        'paper_id': paper_id,
        'title': title,
        'abstract': abstract,
        'body_text': body_text
    }
    
    obj = json.loads(json.dumps(paper), encoding='utf-8')
    body = json.dumps(obj['body_text'], ensure_ascii=True)
    abst = json.dumps(obj['abstract'], ensure_ascii=True)
    body = body.replace("'", "")
    abst = abst.replace("'", "")
    
    sql = str.format("INSERT INTO import.Paper(paper_id, title, abstract, body_text) VALUES({0}, {1}, {2}, {3})", \
       is_dbnull(paper_id), is_dbnull(obj['title']), is_dbnull(abst), is_dbnull(body))
    
    execute_batch(sql)
    batch_info['paper_count'] += 1
    

    for author in authors:
        author_hash = insert_author(author)
        insert_authored(paper_id, author_hash)

        if 'affiliation' in author:
            inst_hash = insert_institution(author['affiliation'])
            insert_affiliation(inst_hash, author_hash)

    for bibref in bib_entries:
        bib = bib_entries[bibref]
        journal_hash = insert_journal(bib['venue'], bib['issn'])
        insert_publishedby(journal_hash, paper_id)

        for author in bib['authors']:
            author_hash = insert_author(author)
            insert_citation(author_hash, paper_id)

    return paper_id


def insert_sql():
    json_papers = read_files(FOLDER)
    i = 0
    for path in json_papers:
        #print(path)
        json_paper = read_json(path)
        insert_paper(json_paper)
        i += 1
        print(i)

insert_sql()
