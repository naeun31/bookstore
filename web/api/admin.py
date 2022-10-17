from flask import Blueprint, request, jsonify
import json
from db import db_session, engine
from model import *
from aladin import crawling

admin_api = Blueprint('admin', __name__)

@admin_api.route('/api/admin/add_books', methods=['POST'])
def add_books():
    params = request.json
    # db_session.add(Book(dct=test))
    # db_session.commit()

    barcodes = params['barcodes']
    shelf_num = params['shelfNum']
    result = to_dict(db_session.query(Book).filter(Book.barcode.in_(barcodes)))
 
    if result:
        for i in result:
            #print(i['barcode'])
            barcodes.remove(i['barcode'])
        
    if barcodes:       
        books = crawling(barcodes)
        books.to_sql('book', engine, if_exists='append')
        db_session.commit()

        return get_book_list()
    else:
        return 'exist'
    
@admin_api.route('/api/admin/get_book_list', methods=['GET'])
def get_book_list():
    bookList = to_dict(db_session.query(Book).all())
    return jsonify(dict(result=bookList))
