# Дан файл с некоторыми данными. Формат файла – произвольный.
# Считайте данные из файла и запишите их в Mongo.
# Реализуйте и выполните следующие запросы:
#
# вывод* первых 10 записей, отсортированных по убыванию по полю salary;
#
# вывод первых 15 записей, отфильтрованных по предикату age < 30, отсортировать по убыванию по полю salary
#
# вывод первых 10 записей, отфильтрованных по сложному предикату:
# (записи только из произвольного города, записи только из трех произвольно взятых профессий), отсортировать по возрастанию по полю age
#
# вывод количества записей, получаемых в результате следующей фильтрации
# (age в произвольном диапазоне, year в [2019,2022], 50 000 < salary <= 75 000 || 125 000 < salary < 150 000).
#
# * – здесь и везде предполагаем вывод в JSON

import json
from pymongo import MongoClient
from bson.json_util import dumps, loads

def connect():
    client = MongoClient()
    db = client['test-datebase']
    return db.person

def get_from_json(filename):
    items = []
    with open(filename, 'r', encoding='utf-8') as f:
        items = json.load(f)
    return items

def insert_many(collection, data):
    result = collection.insert_many(data)
    print(result)

def first_query(collection):
    query = []
    for person in collection.find({}, limit=10).sort({'salary': -1}):
        query.append(person)
    json_data = dumps(query, indent = 2, ensure_ascii=False)
    # json_data = dumps(list_cur, indent = 2)
    with open(f'result_5_1_q1.json', 'w', encoding='utf-8') as f:
        f.write(json_data)


def second_query(collection):
    query = []
    for person in collection.find({"age":{'$lt':30}}, limit=15)\
            .sort({'salary':-1}):
        query.append(person)
    json_data = dumps(query, indent = 2, ensure_ascii=False)
    # json_data = dumps(list_cur, indent = 2)
    with open(f'result_5_1_q2.json', 'w', encoding='utf-8') as f:
        f.write(json_data)


def third_qyery(collection):
    query = []
    for person in collection.find({'city':'Прага',
                                   'job':{"$in":["Учитель","Психолог","Медсестра"]}}, limit =10)\
            .sort({'age':1}):
        query.append(person)
    json_data = dumps(query, indent = 2, ensure_ascii=False)
    # json_data = dumps(list_cur, indent = 2)
    with open(f'result_5_1_q3.json', 'w', encoding='utf-8') as f:
        f.write(json_data)


def fourth_qyery(collection):
    result = collection.count_documents({
        'age':{'$gt':30, "$lt":50},
        'year': {'$in':[2019, 2020, 2021, 2022]},
        '$or' : [
            {'salary': {'$gt':50000, "$lte":75000}},
            {'salary': {'$gt':125000, "$lte":150000}}
        ]
    })
    json_data = dumps(result, indent = 2, ensure_ascii=False)
    # json_data = dumps(list_cur, indent = 2)
    with open(f'result_5_1_q4.json', 'w', encoding='utf-8') as f:
        f.write(json_data)


# data = get_from_json('5_var_7/task_1_item.json')
# insert_many(connect(), data)
first_query(connect())
second_query(connect())
third_qyery(connect())
fourth_qyery(connect())

