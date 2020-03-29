from pyorient import OrientDB
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

papers = client.query("select @rid, title from Paper where paper_id = '1'")

for paper in papers:
    print(paper)

client.close()