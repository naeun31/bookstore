from elasticsearch import Elasticsearch

es = Elasticsearch('http://localhost:9200')



es.search(index='bookstore', query={'match':{'title':'공중그네'}})
