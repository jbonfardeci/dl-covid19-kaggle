from pyorient import OrientDB, OrientRecord
from PySocket import PySocket

# change to your instance address and port  
HOST = "localhost"
PORT = 2424
DATABASE_NAME = "Covid19"
DB_USER = ""
DB_PWD = ""

socket = PySocket(HOST, PORT)
socket.connect()
client = OrientDB(socket)
client.db_open(DATABASE_NAME, DB_USER, DB_PWD) # change to your database name

def get_rid(record: OrientRecord) -> str:
    return record.__dict__['_OrientRecord__o_storage']['rid']

def get_version(record: OrientRecord) -> str:
    return record.__dict__['_OrientRecord__o_storage']['version']
    
# Citation created from #23:11413 to #22:77 
#paper_id = '0a43046c154d0e521a6c425df215d90f3c62681e'
#papers = client.query(str.format("select @rid, paper_id from Paper where paper_id = '{0}'", paper_id))

paper_rid = '#22:77'
author_rid = '#23:11413'
record:OrientRecord = client.query("SELECT @rid FROM Citation WHERE _in = #22:77 AND _out = #23:11413")

print(record)

client.close()