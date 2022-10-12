from flask import g
import sqlite3


DATABASE = '../../bookstore.db'
def get_db():
    db = getattr(g, '_databse', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
    return db