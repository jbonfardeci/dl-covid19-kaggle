from pyorient import OrientDB, OrientRecord
from PySocket import PySocket

HOST = "localhost"
PORT = 2424
DATABASE_NAME = "Covid19Dev"
DB_USER = "root"
DB_PWD = "spark123"
socket = PySocket(HOST, PORT)
socket.connect()
client = OrientDB(socket)
client.db_open(DATABASE_NAME, DB_USER, DB_PWD)

# clusters

journal_cluster_id = client.command("CREATE CLUSTER JournalCluster")[0]
paper_cluster_id = client.command("CREATE CLUSTER PaperCluster")[0]
author_cluster_id = client.command("CREATE CLUSTER AuthorCluster")[0]
inst_cluster_id = client.command("CREATE CLUSTER InstitutionCluster")[0]
authoredby_cluster_id = client.command("CREATE CLUSTER AuthoredByCluster")[0]
publishedby_cluster_id = client.command("CREATE CLUSTER PublishedByCluster")[0]
affiliation_cluster_id = client.command("CREATE CLUSTER AffiliationCluster")[0]
citation_cluster_id = client.command("CREATE CLUSTER CitationCluster")[0]


# vertices
sql_journal_class = [
    str.format("CREATE CLASS Journal extends V CLUSTER {0}", journal_cluster_id),
    "CREATE PROPERTY Journal.name STRING",
    "CREATE PROPERTY Journal.impact_factor FLOAT"
]

sql_paper_class = [
    str.format("CREATE CLASS Paper extends V CLUSTER {0}", paper_cluster_id),
    "CREATE PROPERTY Paper.paper_id STRING",
    "CREATE PROPERTY Paper.title STRING",
    "CREATE PROPERTY Paper.title_short STRING",
    "CREATE PROPERTY Paper.abstract STRING",
    "CREATE PROPERTY Paper.body_text STRING",
    "CREATE PROPERTY Paper.doi STRING",
    "CREATE PROPERTY Paper.has_full_text BOOLEAN",
    "CREATE PROPERTY Paper.journal STRING",
    "CREATE PROPERTY Paper.license STRING",
    "CREATE PROPERTY Paper.ms_paper_id STRING",
    "CREATE PROPERTY Paper.pmcid STRING",
    "CREATE PROPERTY Paper.pubmed_id STRING",
    "CREATE PROPERTY Paper.source_x STRING",
    "CREATE PROPERTY Paper.who_covidence STRING",
    "CREATE PROPERTY Paper.publish_time STRING"
]

sql_author_class = [
    str.format("CREATE CLASS Author extends V CLUSTER {0}", author_cluster_id),
    "CREATE PROPERTY Author.hash_id STRING",
    "CREATE PROPERTY Author.first STRING",
    "CREATE PROPERTY Author.last STRING",
    "CREATE PROPERTY Author.middle STRING",
    "CREATE PROPERTY Author.suffix STRING",
    "CREATE PROPERTY Author.email STRING",
    "CREATE PROPERTY Author.impact_factor FLOAT"
]

sql_Institution_class = [
    str.format("CREATE CLASS Institution extends V CLUSTER {0}", inst_cluster_id),
    "CREATE PROPERTY Institution.hash_id STRING",
    "CREATE PROPERTY Institution.institution STRING",
    "CREATE PROPERTY Institution.laboratory STRING",
    "CREATE PROPERTY Institution.impact_factor FLOAT"
]

# Edges
sql_publishedby_class = [
    str.format("CREATE CLASS PublishedBy EXTENDS E CLUSTER {0}", publishedby_cluster_id)
]

sql_authoredby_class = [
    str.format("CREATE CLASS AuthoredBy EXTENDS E CLUSTER {0}", authoredby_cluster_id)
]

sql_affiliation_class = [
    str.format("CREATE CLASS Affiliation EXTENDS E CLUSTER {0}", affiliation_cluster_id)
]

sql_citation_class = [
    str.format("CREATE CLASS Citation EXTENDS E CLUSTER {0}", citation_cluster_id),
    "CREATE PROPERTY Citation.ref_id STRING",
    "CREATE PROPERTY Citation.title STRING",
    "CREATE PROPERTY Citation.year INTEGER",
    "CREATE PROPERTY Citation.issn STRING"
]

command_list = [
    sql_journal_class,
    sql_paper_class,
    sql_author_class,
    sql_Institution_class,

    sql_publishedby_class,
    sql_authoredby_class,
    sql_affiliation_class,
    sql_citation_class
]

for commands in command_list:
    for cmd in commands:
        res = client.command(cmd)
        print(res)

client.close()
