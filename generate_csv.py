import json
import os.path

import pandas as pd


def extract_data(index, line):
    try:
        row = json.loads(line)

        pdf_url = row['url'][0]

        if 'http://' not in pdf_url:
            pdf_url = 'http://www.dli.ernet.in' + pdf_url

        iterator = iter(row['data'])
        items = dict(zip(iterator, iterator))

        title = items.get('dc.title', '')
        author = items.get('dc.contributor.author', '')

        # pages = items.get('dc.description.totalpages', '')
        # year_published = items.get('dc.date.citation', '')
        # publisher = items.get('dc.publisher', '')
        return title, author, pdf_url

    except Exception as e:
        print(e, line)


filename = 'dli.jl'

csv_file = 'project_chalam.csv'


with open(filename) as fh:
    data = set()
    for index, line in enumerate(fh):
        row = extract_data(index, line)
        if row in data:
            continue
        data.add(row)


columns = ['title', 'author', 'pdf_url']

if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=columns)
    df.to_csv(csv_file, index=False)

df = pd.read_csv(csv_file)
df = df.append(pd.DataFrame(list(data), columns=columns))
df = df.drop_duplicates()
df.to_csv(csv_file, index=False)
