# https://www.elastic.co/kr/downloads/elasticsearch
wget "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-oss-7.10.2-linux-x86_64.tar.gz"
tar zxvf elasticsearch-oss-7.10.2-linux-x86_64.tar.gz
elasticsearch-7.10.2/bin/elasticsearch-plugin install analysis-nori
#start
elasticsearch-7.10.2/bin/elasticsearch -d 

#확인
curl -XGET "http://localhost:9200?pretty"

