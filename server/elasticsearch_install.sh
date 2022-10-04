# https://www.elastic.co/kr/downloads/elasticsearch
wget "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.4.2-linux-x86_64.tar.gz"
tar zxvf elasticsearch-8.4.2-linux-x86_64.tar.gz
vi elasticsearch-8.4.2/config/elasticsearch.yml
##xpack.security.enabled: false
##network.host
##http.port 수정
#확인
curl -XGET "http://localhost:9200?pretty"

#한글형태소분석기 설치
sudo elasticsearch/bin/elasticsearch-plugin install analysis-nori

#background 실행
elasticsearch/bin/elasticsearch -d
