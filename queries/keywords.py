
from pymongo import MongoClient
import pandas as pd

# MongoDB
client = MongoClient('localhost', 27017)
db = client.covid19
collection = db.articles

"""
To perform text search queries, you must have a text index on your 
collection. A collection can only have one text search index, but 
that index can cover multiple fields.
https://docs.mongodb.com/manual/text-search/
"""

tasks = {
    'task1': ['transmission', 'incubation', 'environmental', 'stability'],
    'task2': ['risk', 'factor'],
    'task3': ['virus', 'genetic', 'origin', 'evolution'],
    'task4': ['vaccine', 'therapeutic', 'antibody', 'antibodies'],
    'task5': ['alternative', 'non-pharmaceutical', 'intervention', 'home', 'remedies', 'palliative'],
    'task6': ['diagnostic', 'surveillance', 'signs', 'symptoms'],
    'task7': ['medical', 'care', 'treatment'],
    'task8': ['ethic', 'social', 'science'],
    'task9': ['collaboration', 'data']
}

# Use keywords to search metadata.title, abstract.text, body_text.text
# e.g. { "metadata.title": /(?=.*risk)(?=.*factor)/ig  }
# https://www.ocpsoft.org/tutorials/regular-expressions/and-in-regex/
search_props = ['metadata.title', 'abstract.text', 'body_text.text']

authors = 'metadata.authors'

# rank by reputation of citations/references: journal, authors, publication date (recency)
references = 'bib_entries'



# Regex AND pattern
# /^(?=.*\bword1\b)(?=.*\bword2\b)(?=.*\bword3\b).*$/m

client.close()