from pyorient import OrientDB, OrientRecord
from PySocket import PySocket

# change to your instance address and port  
HOST = "localhost"
PORT = 2424
DATABASE_NAME = "Covid19"
DB_USER = "admin"
DB_PWD = "admin"

socket = PySocket(HOST, PORT)
socket.connect()
client = OrientDB(socket)
client.db_open(DATABASE_NAME, DB_USER, DB_PWD) # change to your database name

def get_rid(record: OrientRecord) -> str:
    return record.__dict__['_OrientRecord__rid']
    
paper_id = '0a43046c154d0e521a6c425df215d90f3c62681e'
papers = client.query(str.format("select * from Paper where paper_id = '{0}'", paper_id))

if len(papers) > 0:
    rid = get_rid(papers[0])
    print(rid)
else:
    print('not found')

client.close()