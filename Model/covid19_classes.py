from pyorient.ogm import declarative, Config
from pyorient.ogm.graph import String, Boolean, Link, Float
from typing import Dict
import json

# Initialize Registries
Node = declarative.declarative_node()
Relationship = declarative.declarative_relationship()

class Journal(Node):
    name = String()
    impact_factor = Float()

class Paper(Node):
    paper_id = String()
    title = String()
    title_short = String()
    abstract = String()
    body_text = String()
    doi = String()
    has_full_text = Boolean()
    license = String()
    ms_paper_id = String()
    pmcid = String()
    pubmed_id = String()
    source_x = String()
    who_covidence = String()
    publish_time = String()

class Author(Node):
    hash_id = String()
    first = String()
    last = String()
    middle = String()
    suffix = String()
    email = String()
    impact_factor = Float()

class Institution(Node):
    hash_id = String()
    laboratory = String()
    institution_name = String()
    impact_factor = Float()

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
    ref_id = String()
    title = String()
    year = String()
    issn = String()