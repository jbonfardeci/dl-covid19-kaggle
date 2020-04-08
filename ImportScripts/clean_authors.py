import pandas as pd
import re
import json
import hashlib

folder = "C:\\Users\\bonfardeci-j\\source\\dl-covid19-kaggle-contest\\Data\\"

def trim(s):
    return re.sub(r'(^s\+|\s+$)', '', str(s))

def is_empty(s):
    return s == None or s == 'NULL' or trim(s) == '' 

def clean_str(s):
    if s == None or str(s) == 'nan':
        return None

    s = re.sub(r'[^a-zA-Z0-9\s.-_#:,]', '', str(s))
    return None if len(s) == 0 else s

def hash_strings(strings):
    a = [trim(s) for s in strings if not is_empty(s)]
    return hashlib.md5(''.join(a).encode()).hexdigest()

def authors_to_list(s):
    """
    Parse the different list types of authors in CSV data.
    """
    s = re.sub(r'[^a-zA-Z0-9\s\,\'\"\;]', '', str(s), re.DOTALL)
    
    return s
    
df = pd.read_csv(folder+"all_sources_metadata_2020-03-13_clean.csv")
authors = df['authors']

cleaned = list(map(authors_to_list, authors.values))
#cleaned_df = pd.DataFrame(data=cleaned)

print(cleaned[:1000])
