from pymongo import MongoClient


def get_db():
    conn = MongoClient('192.168.0.113', 27017)
    db = conn.mydb
    return db