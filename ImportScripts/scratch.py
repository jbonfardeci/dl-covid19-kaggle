import re
import json

s = "article's"
def trim(s) -> str:
    return re.sub(r'(^\s+|\s+$)', '', str(s), )

def clean_str(s:str) -> str:
    if s == None or str(s) == 'nan':
        return None

    #c = re.compile(r'[^a-zA-Z0-9\s.-_#:,\']')
    s = re.escape(s)
    s = trim( re.sub(r'[^a-zA-Z0-9\s.-_#:,\']', '', str(s), re.MULTILINE))
    s = re.sub( r'(^\'+|\'+$)', "", s, re.MULTILINE)
    s = re.sub( r'\'+', "\\'", s, re.DOTALL|re.MULTILINE)
    return None if len(s) == 0 else s

print(clean_str(s))
