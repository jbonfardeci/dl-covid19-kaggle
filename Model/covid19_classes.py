from pyorient.ogm import declarative
import json

# Initialize Registries
Node = declarative.declarative_node()
Relationship = declarative.declarative_relationship()

class Paper(Node):
    """
    Paper Vertex
    """
    def __init__(self, paper_id=None, title=None):
        self.paper_id = paper_id
        self.title = title

    abstract = None
    body_text = None

    def to_json(self):
        return json.dumps(self.__dict__)


class Author(Node):
    """
    Author Vertex
    """
    def __init__(self, first=None, last=None):
        self.first = first
        self.last = last

    middle = None
    suffix = None
    email = None

    def to_json(self):
        return json.dumps(self.__dict__)

class BibEntry(Node):
    """
    BibEntry Vertex
    """

    def __init__(self, paper_id):
        self.paper_id = paper_id

    ref_id = None
    title = None
    year = None
    venue = None
    issn = None

class AuthorWrote(Relationship):
    pass 

class AuthorCited(Relationship):
    pass

class Citation(Relationship):
    pass






