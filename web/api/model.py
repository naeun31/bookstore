from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy.dialects.sqlite import insert

class Model():
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

def to_dict(result):
    return [r.as_dict() for r in result]

class Book(Base, Model):
    __tablename__ = 'book'
    title = Column(Text)
    barcode = Column(Text, primary_key=True)
    author = Column(Text)
    price = Column(Text)
    image = Column(Text)
    category2 = Column(Text)
    publish = Column(Text)
    published_date = Column(Text)
    shelf_num = Column(Text)

    def __init__(self, *args, **kwargs):
        keys = kwargs['dct'].keys()
        dct = kwargs['dct']
        self.title = dct['title'] if 'title' in keys else None
        self.barcode = dct['barcode'] if 'barcode' in keys else None
        self.author = dct['author'] if 'author' in keys else None
        self.price = dct['price'] if 'price' in keys else None
        self.image = dct['image'] if 'image' in keys else None
        self.category2 = dct['category2'] if 'category2' in keys else None
        self.publish = dct['publish'] if 'publish' in keys else None
        self.published_date = dct['published_date'] if 'published_date' in keys else None
        self.shelf_num = dct['shelf_num'] if 'shelf_num' in keys else None

class Shelf(Base, Model):
    __tablename__ = 'shelf'
    num = Column(Text, primary_key=True)

    def __init__(self, *args, **kwargs):
        print(1, args, type(args))
        print(1, kwargs, type(kwargs))
        self.num = args[0]['num']

    def insert(shelf):
        stmt = (
            insert(Shelf).values(num=shelf.num)
        )
        print(stmt)

class BookShelf(Base, Model):
    __tablename__ = 'bookshelf'
    num = Column(Text, primary_key=True)
    barcode = Column(Text, primary_key=True)

    def __init__(self, *args, **kwargs):
        keys = args[0].keys()
        dct = args[0]
        self.num = dct['num'] if 'num' in keys else None
        self.barcode = dct['barcode'] if 'barcode' in keys else None

    def insert(bookshelf):
        stmt = (
            insert(BookShelf).values(num=bookshelf.num, barcode=bookshelf.barcode)
        )
        print(stmt)
