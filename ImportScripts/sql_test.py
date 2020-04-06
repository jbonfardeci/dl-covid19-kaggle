import pyodbc 

commands = []
commands.append("INSERT INTO covid19.import.Paper(paper_id, title) VALUES ('1', 'test 1')")
commands.append("INSERT INTO covid19.import.Paper(paper_id, title) VALUES ('2', 'test 2')")
commands.append("INSERT INTO covid19.import.Paper(paper_id, title) VALUES ('3', 'test 3')")

batch = ';\r\n'.join(commands)

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=ZBOOK27\MSSQLSERVER17;'
                      'Database=covid19;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
cursor.execute(batch)
conn.commit()