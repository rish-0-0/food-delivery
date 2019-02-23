import pymongo
from constants import *

def insert_into_db(dict):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[DATABASE_VAR]
    mycol = mydb['order_id']

    mycol.insert_one(dict)

def query_from_db():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[DATABASE_VAR]
    mycol = mydb['order_id']

    mydoc = list(mycol.find())

    return mydoc

def uptdate_in_db(id,new_query):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[DATABASE_VAR]
    mycol = mydb["order_id"]
    id_val = {ORDER_ID_VAR:id}
    newvalues = {"$set": new_query}

    mycol.update(id_val, newvalues)

def drop_col():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[DATABASE_VAR]
    mycol = mydb["order_id"]

    mycol.drop()
