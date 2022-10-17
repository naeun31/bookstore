"""
:filename: app.py
:author: XXX
:last update: 2022.08.30
:CHANGELOG:
    ============== ========== ========================================================================
    수정일          수정자      수정내용
    ============== ========== ========================================================================
    2022.10.04     XXX      최초작성
    ============== ========== ========================================================================

:DESC: Flask webapp

"""
import os
import flask
from flask import Flask, g, request, jsonify, Blueprint, make_response, render_template, current_app
import redis
import json
from sqlalchemy import create_engine
from admin import admin_api
#from elasticsearch import Elasticsearch
from db import db_session

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(admin_api)
try:
    app.config['db'] = redis.Redis(host='localhost', port=6379, db=0)
    #app.config['es'] = Elasticsearch('http://localhost:9200/bookstore')
except:
    app.config['db'] = redis.Redis(host='xxx.xxx.xxx.xxx', port=6379, db=0)
    #app.config['es'] = Elasticsearch('http://localhost:9200/bookstore')


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/api')
def hello_world():
    return 'Hello API!!!'

@app.route('/search')
def search():
    pass
    #return app.config['es'].search(query={'match':{'title':'공중그네'}})

@app.route('/test', methods=['POST','GET'])
def get_observation():
    try:
        db = current_app.config['db']
        if len(request.form) > 0:
            request.args= request.form
        keys = request.args.to_dict().keys()
        values = [json.loads(x.decode('utf-8')) if type(x)==bytes else [] for x in db.mget(keys)]
        data = {k:v for k, v in zip(keys, values)}
        return jsonify(dict(result='success', data=data, msg=''))
    except Exception as e:
        return jsonify(dict(result='fail', data=None, msg=str(e)))


if __name__ == '__main__':
    app.run(debug=True)
