
bib_entries = {
    "BIBREF0": {
        "ref_id": "b0",
        "title": "Native morphology of influenza virions",
        "authors": [
            {
                "first": "Noda",
                "middle": [],
                "last": "Tjfim",
                "suffix": ""
            }
        ],
        "year": 2012,
        "venue": "",
        "volume": "2",
        "issn": "",
        "pages": "",
        "other_ids": {}
    }
}

for bib in bib_entries:
    o = bib_entries[bib]

    ref_id = o['ref_id']
    bib_title = o['title']
    year = o['year']
    venue = o['venue']
    issn = o['issn']
    bib_authors = o['authors']

    for auth in bib_authors:
        print(auth)

    print(bib_title)