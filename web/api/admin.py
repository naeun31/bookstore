from flask import Blueprint, request, jsonify
import json
from db import db_session, engine
from model import *
from aladin import crawling as aladin_crawling
from kyobobook import crawling as kyobobook_crawling
import pandas as pd
from copy import copy
from elasticsearch import Elasticsearch


admin_api = Blueprint('admin', __name__)

@admin_api.route('/api/admin/add_books', methods=['POST'])
def add_books():
    params = request.json
    # db_session.add(Book(dct=test))
    # db_session.commit()

    es = Elasticsearch('http://localhost:9200')
    barcodes = set(copy(params['barcodes']))
    shelf_num = copy(params['shelfNum'])
    result = to_dict(db_session.query(Book).filter(Book.barcode.in_(barcodes)))

    new_barcodes = (barcodes - set([x['barcode'] for x in result]))
    try:
        books = aladin_crawling(new_barcodes)
    except:
        try:
            books = kyobobook_crawling(new_barcodes)
        except:
            books = kyobobook_crawling(new_barcodes)
    books.to_sql('book', engine, if_exists='append', index=False)
    db_session.commit()
    for i in books.index:
       book = dict(books.iloc[i])
       print(book)
       es.index(index="bookstore", body=book, pretty=True, id=book['barcode'])
    #서가등록
    if barcodes:
        for barcode in barcodes:
            doc = es.get(id=barcode, index='bookstore')['_source']
            print(doc)
            if 'shelf_num' not in doc.keys():
                doc['shelf_num'] = shelf_num
            elif doc['shelf_num'] == None:
                doc['shelf_num'] = shelf_num
            else:
                if len(doc['shelf_num']) == 0: doc['shelf_num'] = shelf_num
                else: doc['shelf_num'] = doc['shelf_num'] + ', ' + shelf_num
            print(doc)
            es.index(index="bookstore", body=doc, pretty=True, id=barcode)
        return get_book_list()
    else:
        return 'exist'

    """
    #서가등록여부 확인
    print('서가등록여부확인',shelf_num)
    result = to_dict(db_session.query(Shelf).filter(Shelf.num == shelf_num))
    if len(result)==0:
        shelf = Shelf(dict(num=shelf_num))
        Shelf.insert(shelf)
    print('서가등록여부확인끝')
    #서가 도서등록 시작
    print('3'*30)
    print(params['barcodes'])
    print([dict(barcode=x, num=shelf_num) for x in params['barcodes']])
    for x in [dict(barcode=x, num=shelf_num) for x in params['barcodes']]:
        bookshelf = BookShelf(x)
        BookShelf.insert(bookshelf)
    #db_session.commit()
    """

@admin_api.route('/api/admin/get_book_list', methods=['GET'])
def get_book_list():
    bookList = to_dict(db_session.query(Book).all())
    return jsonify(dict(result=bookList))



@admin_api.route('/api/admin/remove_books', methods=['POST'])
def remove_books():
    barcodes = set(request.form['barcodes'].split("|"))
    shelf_num = request.form['shelf_num']
    result = to_dict(db_session.query(Book).filter(Book.barcode.in_(barcodes)))
    for i, r in enumerate(result):
        r['shelf_num'] = str(r['shelf_num']).replace(', ' + shelf_num, '').replace(shelf_num, '')
        result[i] = r
    es = Elasticsearch('http://localhost:9200')
    sql = "update book set shelf_num = ? where barcode = ?"
    for data in result:
        engine.execute(sql, (data['shelf_num'], data['barcode']))
        es.index(index='bookstore', body=data, id=data['barcode'])
    return {'result':True}

@admin_api.route('/api/admin/save_book', methods=['POST'])
def save_book():
    p = dict(request.form)
    sql = "update book set title=?, author=?, publish=?, published_date=?, price=?, shelf_num=? where barcode=?"
    engine.execute(sql, (p['title'], p['author'], p['publish'], p['published_date'], p['price'], p['shelf_num'], p['barcode']) )
    es = Elasticsearch('http://localhost:9200')
    doc = es.get(index='bookstore', id='9791186009222')['_source']
    doc.update(p)
    es.index(index='bookstore', body=doc, id=doc['barcode'])
    print(doc)
    return {'result':True}

