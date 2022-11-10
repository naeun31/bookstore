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
import sqlite3



DATABASE = '/workspace/bookstore/bookstore.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = make_dicts
    return db

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(admin_api)
try:
    app.config['db'] = redis.Redis(host='localhost', port=6379, db=0)
    #app.config['es'] = Elasticsearch('http://localhost:9200/bookstore')
    #app.config['sqlite'] = sqlite3.connect('bookstore.db')
    #g.db = sqlite3.connect("bookstore.db")
    #g.db.row_factory = make_dicts    
    #g.cur = g.db.cursor()
    #app.config['sqlite'].row_factory = make_dicts    
    #app.config['cursor'] = app.config['sqlite'].cursor()
except Exception as e:
    print('error')
    print(str(e))
    #app.config['db'] = redis.Redis(host='xxx.xxx.xxx.xxx', port=6379, db=0)
    #app.config['es'] = Elasticsearch('http://localhost:9200/bookstore')


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/api')
def hello_world():
    return 'Hello API!!!'

@app.route('/api/search')
def search():
    pass
    #return app.config['es'].search(query={'match':{'title':'공중그네'}})

@app.route('/api/test', methods=['POST','GET'])
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



@app.route('/api/shelf', methods=['POST','GET'])    
def shelf():    
    #return str(current_app.config.keys())
    sql = """SELECT num FROM shelf order by num"""   
    return get_db().cursor().execute(sql).fetchall()


@app.route('/api/book', methods=['POST','GET'])    
def book():
    if len(request.form) > 0:
        request.args= request.form    
    sql = """SELECT * FROM book WHERE barcode = :barcode"""
    return get_db().cursor().execute(sql, {'barcode':request.args['barcode']}).fetchall()

@app.route('/api/bookshelf', methods=['POST','GET'])    
def bookshelf():
    if len(request.form) > 0:
        request.args= request.form    
    sql = """SELECT a.num, b.* FROM bookshelf a, book b WHERE a.barcode = b.barcode AND a.num = :num order by num, published_date DESC, title, publish"""
    return get_db().cursor().execute(sql, {'num':request.args['num']}).fetchall()

#shelf insert
def shelf_insert(num):
    sql =  """INSERT INTO shelf (num) values (:num)"""
    try:
        get_db().cursor().execute(sql, {'num':num})
        get_db().commit()
    except:
        pass

#shelf delete
def shelf_delete(num):
    sql =  """SELECT COUNT(*) cnt FROM bookshelf WHERE num = :num"""
    if app.config['cursor'].execute(sql, {'num':num}).fetchone()[0] <= 0:
        sql = """DELETE FROM shelf WHERE num = :num"""
    try:
        get_db().cursor().execute(sql, {'num':num})
        get_db().commit()
    except:
        pass

#book insert
def book_insert(book):
    try:
        sql = "INSERT INTO book (" + ' ,'.join(book.keys()) + ") VALUES (:" + ' ,:'.join(book.keys()) + ")"
        get_db().cursor().execute(sql, book)
        return True
    except:
        return False

#bookshelf insert
def bookshelf_insert(num, barcode):
    if num == None or num == barcode == None or num == '' or barcode == '': return False
    sql = """SELECT num FROM shelf WHERE num = :num"""
    if get_db().cursor().execute(sql, {'num':num}).fetchone() == None:
        sql = """INSERT INTO shelf (num) VALUES (:num)"""
        get_db().cursor().execute(sql, {'num':num})
    try:
        sql = """INSERT INTO bookshelf (num, barcode) VALUES (:num, barcode)"""
        get_db().cursor().execute(sql, book)
        get_db().commit()
        return True
    except:
        return False


if __name__ == '__main__':
    app.run(debug=True)
