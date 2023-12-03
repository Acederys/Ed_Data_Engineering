# Дан файл с некоторыми данными. Формат файла –
# произвольный, не совпадает с тем, что был в первом/втором заданиях.
# Необходимо считать данные и добавить их к той коллекции, куда были
# записаны данные в первом и втором заданиях. Выполните следующие запросы:
# удалить из коллекции документы по предикату:
# salary < 25 000 || salary > 175000
# увеличить возраст (age) всех документов на 1
# поднять заработную плату на 5% для произвольно выбранных профессий
# поднять заработную плату на 7% для произвольно выбранных городов
# поднять заработную плату на 10% для выборки по сложному предикату
# (произвольный город, произвольный набор профессий, произвольный диапазон возраста)
# удалить из коллекции записи по произвольному предикату
import msgpack
import json
import csv
from pymongo import MongoClient
from bson.json_util import dumps, loads

def connect():
    client = MongoClient()
    db = client['test-datebase']
    return db.person

def get_from_csv(filename):
    with open(filename, 'rb') as mp_file:
        items = msgpack.load(mp_file)
    return items
def insert_many(collection, data):
    result = collection.insert_many(data)
    print(result)

# удалить из коллекции документы по предикату:
# salary < 25 000 || salary > 175000
def first_query(collection):
    result = collection.delete_many({
        '$or' : [
            {'salary': {'$lt':25_000}},
            {'salary':{'$gt':175_000}}
        ]
    })
    print(result)
# увеличить возраст (age) всех документов на 1
def second_query(collection):
    result = collection.update_many({},{
        '$inc': {
            'age': 1
        }
    })
    print(result)
# поднять заработную плату на 5% для произвольно выбранных профессий
def third_query(collection):
    filter = {
        "job" : {"$in": ["Программист", "Врач", "Учитель"]}
    }
    update = {
            "$mul" : {
                'salary': 1.05
        }
    }
    result = collection.update_many(filter, update)
    print(result)
# поднять заработную плату на 7% для произвольно выбранных городов
def fourth_query(collection):
    filter = {
        "city" : {"$in": ["Эль-Пуэрто-де-Санта-Мария", "Осера", "Сеговия"]}
    }
    update = {
            "$mul" : {
                'salary': 1.07
        }
    }
    result = collection.update_many(filter, update)
    print(result)
# поднять заработную плату на 10% для выборки по сложному предикату
# (произвольный город, произвольный набор профессий, произвольный диапазон возраста)
def fifth_query(collection):
    filter = {
        "city" : {"$in": ["Эль-Пуэрто-де-Санта-Мария", "Осера", "Сеговия"]},
        "job" : {"$in": ["Программист", "Врач", "Учитель"]},
        "$or": [
                {'age': {"$gt":18, '$lt':25}},
                {'age': {"$gt":50, '$lt':65}}
            ]
    }
    update = {
            "$mul" : {
                'salary': 1.1
        }
    }
    result = collection.update_many(filter, update)
    print(result)
# удалить из коллекции записи по произвольному предикату
def sixth_query(collection):
    result = collection.delete_many({
        '$or' : [
            {'age': {'$lt':60}},
            {'age':{'$gt':95}}
        ]
    })
    print(result)
# data = get_from_csv('5_var_7/task_3_item.msgpack')
# insert_many(connect(), data)
first_query(connect())
second_query(connect())
third_query(connect())
fourth_query(connect())
fifth_query(connect())
sixth_query(connect())
