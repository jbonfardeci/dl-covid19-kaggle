import re
import json
import pandas as pd
import hashlib

def trim(s) -> str:
    if s == None:
        return s

    return re.sub(r'(^\s+|\s+$)', '', str(s))

def is_empty(s) -> bool:
    return s == None or trim(s) == '' 

def clean_str(s:str) -> str:
    if s == None or str(s) == 'nan':
        return None

    s = re.sub(r'[^a-zA-Z0-9\s.-_#:,]', '', str(s), re.DOTALL)
    return None if len(s) == 0 else s

def to_bool(s):
    rx = re.match("(1|true|yes)", trim(str(s).lower()), re.DOTALL)
    if rx:
        return rx.group() in ['1', 'yes', 'true']

    return False

def hash_author(author) -> str:

    def _in(prop:str, o) -> str:
        return trim(o[prop]) if prop in o else ''

    f = _in('first', author)
    l = _in('last', author)
    m = _in('middle', author)

    combined = str.format("{0}{1}{2}", f, l, m)
    hashed = hashlib.md5(combined.encode())
    return hashed.hexdigest()

def hash_strings(strings) -> str:
    a = [trim(s) for s in strings if not is_empty(s)]
    return hashlib.md5(''.join(a).encode()).hexdigest()

def authors_to_list(paper_id:str, s:str):
    """
    Parse the different list types of authors in CSV data.
    """
    s = str(s)

    def strip_quotes(s):
        return trim(re.sub(r'\"', '', s, re.DOTALL))

    def _to_dict(s):
        if s == None:
            return {} 

        auth = {
            "paper_id": paper_id,
            "hash_id": None,
            "first": None,
            "last": None,
        }

        if s.find(',') > -1:
            names = list( map(strip_quotes, s.split(',')) )
            auth['first'] = names[1]
            auth['last'] = names[0]

        else:
            auth['last'] = strip_quotes(s)

        auth['hash_id'] = hash_author(auth)
        return auth

    if s == None or len(trim(s)) == 0:
        return []

    s = re.sub(r'\',\s\'', ';', s, re.DOTALL) 
    s = re.sub(r'[^a-z0-9A-Z\-,\s\;]', '', s, re.DOTALL)         
    lst = list(map(_to_dict, s.split(';')))

    return lst


def import_csv_metadata():
    file_path = "/home/spark/Documents/repos/dl-covid19-kaggle-contest/Data/all_sources_metadata_2020-03-13_clean.csv"
    df = pd.read_csv(file_path)
    authors = df[['sha', 'authors', 'has_full_text']].values.tolist()
    
    data = []

    i = 0
    for row in authors:
        if to_bool(row[2]) or str(row[1]) == 'nan':
            continue
        
        paper_id = str.format('na_paper_id_{0}', i) if str(row[0]) == 'nan' else row[0]
        lst = authors_to_list(paper_id, row[1])
        data.extend(lst)
        i += 1

    
    author_df = pd.DataFrame(columns=['paper_id', 'hash_id', 'first', 'last'], data=data)
    author_df.to_csv("/home/spark/Documents/repos/dl-covid19-kaggle-contest/Data/authors.csv")

import_csv_metadata()
