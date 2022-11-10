import json
import sqlite3
from elasticsearch import Elasticsearch


es = Elasticsearch('http://localhost:9200')
with open('bookstore.json') as f:
    mapping = json.load(f)

#index 생성
es.indices.create(index='bookstore', body=mapping)


#with open('data.json') as f:
#    data = json.load(f)

#book indexing
sql = "select * from book"
con = sqlite3.Connection('bookstore.db')
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

con.row_factory = make_dicts
cur = con.cursor()
data = cur.execute(sql).fetchall()

for doc in data:
    doc_id = doc['barcode']
    es.index(index="bookstore", body=doc, pretty=True, id=doc_id)

#search test
es.search(index='bookstore', query={'match':{'title':'지구별'}})

es.search(index='bookstore', query={'multi_match':{'query':'김승호'}})



	