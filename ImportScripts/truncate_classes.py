from pyorient import OrientDB, OrientRecord
from PySocket import PySocket

HOST = "localhost"
PORT = 2424
DATABASE_NAME = "Covid19Dev"
DB_USER = "admin"
DB_PWD = "admin"

def truncate_clusters():
    # Open DB connection
    socket = PySocket(HOST, PORT)
    socket.connect()
    client = OrientDB(socket)
    client.db_open(DATABASE_NAME, DB_USER, DB_PWD) # change to your database name

    client.command("TRUNCATE CLASS Journal UNSAFE")
    client.command("TRUNCATE CLASS Paper UNSAFE")
    client.command("TRUNCATE CLASS Author UNSAFE")
    client.command("TRUNCATE CLASS Institution UNSAFE")

    client.command("TRUNCATE CLASS PublishedBy UNSAFE")
    client.command("TRUNCATE CLASS AuthoredBy UNSAFE")
    client.command("TRUNCATE CLASS Affiliation UNSAFE")
    client.command("TRUNCATE CLASS Citation UNSAFE")

    print('All clusters truncated.')

    client.close()


def confirm_truncate():
    msg = "DANGER! This will delete all data. Are you sure you want to continue?"
    prompt = '%s [%s]|%s: ' % (msg, 'n', 'y')
        
    while True:
        ans = input(prompt)
        if not ans:
            return msg
        if ans.lower() not in ['y', 'n']:
            print('Enter y or n.')
            continue
        if ans.lower() == 'y':
            print('Truncating all clusters.')
            truncate_clusters()
            return True
        if ans.lower() == 'n':
            print('Operation cancelled.')
            return False

confirm_truncate()

