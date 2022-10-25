import sqlite3
import pandas as pd
from elasticsearch import Elasticsearch

#curl -XPUT "http://localhost:9200/bookstore/" -H 'content-Type: application/json' -d @bookstore.json 
es = Elasticsearch('http://localhost:9200')
#es.indices.create(index='bookstore')
con = sqlite3.connect('../bookstore.db')
df = pd.read_sql('select * from book')
[es.index(index='bookstore', body=x) for x in df.to_dict('records')]
con.close()
es.close()
