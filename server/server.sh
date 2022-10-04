pip install redis flask pymysql gunicorn sqlalchemy

#sudo apt-get install nginx


#nohup gunicorn app:app -b 0.0.0.0:8000 -w 2 --timeout=10 -k gevent >> ../app.log &
