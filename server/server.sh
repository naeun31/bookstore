#install python package
pip install redis flask pymysql gunicorn sqlalchemy gevent bs4 pandas

#install nginx
#sudo apt-get install nginx

#start gunicorn flask app
#nohup gunicorn app:app -b 0.0.0.0:8000 -w 2 --timeout=10 -k gevent >> ../app.log &

#install elasticsearch
# curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
# echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
# sudo apt update
# sudo apt install elasticsearch
# sudo systemctl start elasticsearch
# sudo systemctl enable elasticsearch

