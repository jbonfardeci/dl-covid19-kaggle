from pyorient.ogm import declarative
from typing import Dict
import json

# Initialize Registries
Node = declarative.declarative_node()
Relationship = declarative.declarative_relationship()

class Paper(Node):
    """
    Paper Vertex
    """
    def __init__(self, paper_id:str):
        self.paper_id = paper_id

    title:str = None
    abstract:str = None
    body_text:str = None
    doi: str = None
    has_full_text: bool = False
    journal: str = None
    license: str = None
    ms_paper_id: str = None
    pmcid: str = None
    pubmed_id: str = None
    source_x: str = None
    who_covidence: str = None
    publish_time: str = None

class Author(Node):
    """
    Author Vertex
    """
    first:str = None
    last:str = None
    middle:str = None
    suffix:str = None
    email:str = None
    hash_id:str = None

class BibEntry(Node):
    """
    BibEntry Vertex
    """
    def __init__(self, paper_id:str):
        self.paper_id = paper_id

    ref_id:str = None
    title:str = None
    year:str = None
    venue:str = None
    issn:str = None