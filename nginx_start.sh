#!/usr/bin/bash
sudo cp nginx.conf /etc/nginx/nginx.conf
nohup python web/api/app.py > /dev/null &
export NGINX_DOCROOT_IN_REPO=web/www
nginx
