from pyorient import OrientDB, OrientRecord
from PySocket import PySocket

# change to your params
HOST = "localhost"
PORT = 2424
DATABASE_NAME = "Covid19"
DB_USER = "admin"
DB_PWD = "admin"

# Open DB connection
socket = PySocket(HOST, PORT)
socket.connect()
client = OrientDB(socket)
client.db_open(DATABASE_NAME, DB_USER, DB_PWD) # change to your database name

client.command("TRUNCATE CLASS Affiliation UNSAFE")
client.command("TRUNCATE CLASS Author UNSAFE")
client.command("TRUNCATE CLASS BibEntry UNSAFE")
client.command("TRUNCATE CLASS Paper UNSAFE")

client.command("TRUNCATE CLASS AuthorBibEntry UNSAFE")
client.command("TRUNCATE CLASS AuthorAffiliation UNSAFE")
client.command("TRUNCATE CLASS AuthorPaper UNSAFE")
client.command("TRUNCATE CLASS BibEntryPaper UNSAFE")


client.close()