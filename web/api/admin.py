from flask import Blueprint, request, jsonify
import json
from db import db_session, engine
from model import *
from aladin import crawling
import pandas as pd
from copy import copy

admin_api = Blueprint('admin', __name__)

@admin_api.route('/api/admin/add_books', methods=['POST'])
def add_books():
    params = request.json
    # db_session.add(Book(dct=test))
    # db_session.commit()

    barcodes = copy(params['barcodes'])
    shelf_num = copy(params['shelfNum'])
    result = to_dict(db_session.query(Book).filter(Book.barcode.in_(barcodes)))
    #book master 등록여부 확인
    if result:
        for i in result:
            #print(i['barcode'])
            barcodes.remove(i['barcode'])
    #book master 미등록건 등록
    if barcodes:       
        books = crawling(barcodes)
        books.to_sql('book', engine, if_exists='append')
        db_session.commit()
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
