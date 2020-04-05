from pyorient.ogm import declarative, Config
from pyorient.ogm.graph import String, Boolean, Link, Float
from typing import Dict
import json

# Initialize Registries
Node = declarative.declarative_node()
Relationship = declarative.declarative_relationship()

class Journal(Node):
    name = None
    impact_factor = None

class Paper(Node):
    paper_id = None
    title = None
    title_short = None
    abstract = None
    body_text = None
    doi = None
    has_full_text = None
    license = None
    ms_paper_id = None
    pmcid = None
    pubmed_id = None
    source_x = None
    who_covidence = None
    publish_time = None
    authors = None

class Author(Node):
    hash_id = None
    first = None
    last = None
    middle = None
    suffix = None
    email = None
    impact_factor = None

class Institution(Node):
    hash_id = None
    laboratory = None
    institution_name = None
    impact_factor = None

class PublishedBy(Relationship):
    # 1-n
    # from: Journal, to: Paper
    # journal paper is published in
    # journal has many papers
    _in = Link(Journal)
    _out = Link(Paper)

class AuthoredBy(Relationship):
    # 1-n
    # from: Paper, to: Author
    # author who co-wrote paper
    # authors write many papers
    _in = Link(Paper)
    _out = Link(Author)

class Affiliation(Relationship):
    # 1-n
    # from: Institution, to: Author
    # author affiliated with institution
    # institution has many authors
    institution = Link(Institution)
    author = Link(Author)

class Citation(Relationship):
    # 1-n
    # from: Paper, to: Author
    # author cited by paper
    # paper cites many authors and institutions
    _in = Link(Author)
    _out = Link(Paper)
    ref_id = None
    title = None
    year = None
    issn = None