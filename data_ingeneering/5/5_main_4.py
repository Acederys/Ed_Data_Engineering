# Самостоятельно выбрать предметную область.
# Подобрать пару наборов данных разных форматов.
# Заполнение данных в mongo осуществляем из файлов.
# Реализовать выполнение по 5 запросов в каждой категорий:
# выборка (задание 1),
# выбора с агрегацией (задание 2)
# обновление/удаление данных (задание 3).
import json
import csv
import pandas as pd
from pymongo import MongoClient
from bson.json_util import dumps, loads

def connect():
    client = MongoClient()
    db = client['test-datebase']
    return db.finanse
# добавление данных csv в коллекцию
def get_from_csv(filename):
    items = []
    with open(filename, 'r', encoding='utf-8') as f:

        data_csv = csv.reader(f, delimiter=';', quotechar='|')
        next(data_csv)
        for i in data_csv:
            item = {
                'Year': int(i[0]),
                'Industry_aggregation_NZSIOC': i[1],
                'Industry_code_NZSIOC': i[2],
                'Industry_name_NZSIOC': i[3],
                'Units': i[4],
                'Variable_code': i[5],
                'Variable_name' : i[6],
                'Variable_category': i[7],
                'Value' : int(i[8].replace(',','')),
                'Industry_code_ANZSIC06': i[9]
            }
            items.append(item)
        # print(items)
    return items
def insert_many(collection, data):
    result = collection.insert_many(data)
    print(result)
# вывод* первых 10 записей, отсортированных по убыванию по полю Industry_aggregation_NZSIOC;
def first_query(collection):
    query = []
    for finanse in collection.find({}, limit=10).sort({'Industry_aggregation_NZSIOC': -1}):
        query.append(finanse)
    json_data = dumps(query, indent = 2, ensure_ascii=False)
    with open(f'result_5_4_q1.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
# вывод первых 15 записей, отфильтрованных по предикату Value > 10000,
# отсортировать по убыванию по полю Industry_aggregation_NZSIOC


def second_query(collection):
    query = []
    for finanse in collection.find({"Value":{'$gt':10000}}, limit=15)\
            .sort({'Industry_aggregation_NZSIOC':-1}):
        query.append(finanse)
    json_data = dumps(query, indent = 2, ensure_ascii=False)
    with open(f'result_5_4_q2.json', 'w', encoding='utf-8') as f:
        f.write(json_data)


# вывод первых 10 записей, отфильтрованных по сложному предикату:
# (записи только из произвольного Units,
# записи только из  произвольно взятых Variable_category),
# отсортировать по возрастанию по полю Value

def third_qyery(collection):
    query = []
    for person in collection.find({'Units':'Dollars (millions)',
                                   'Variable_category':{"$in":["Financial performance","Financial ratios"]}}, limit =10)\
            .sort({'Value':-1}):
        query.append(person)
    json_data = dumps(query, indent = 2, ensure_ascii=False)
    with open(f'result_5_4_q3.json', 'w', encoding='utf-8') as f:
        f.write(json_data)

# вывод количества записей, получаемых в результате следующей фильтрации
#(Value в произвольном диапазоне, Industry_aggregation_NZSIOC).
def fourth_qyery(collection):
    result = collection.count_documents({
        'Value':{'$gt':10000, "$lt":50000},
        'Industry_aggregation_NZSIOC': {'$in':['Level 4', 'Level 2']}
    })
    json_data = dumps(result, indent = 2, ensure_ascii=False)
    with open(f'result_5_4_q4.json', 'w', encoding='utf-8') as f:
        f.write(json_data)

#Добавление данных
def get_from_json(filename):
    items = []
    with open(filename, 'r', encoding='utf-8') as f:
        elem = json.load(f)
    for i in elem:
        if i['Value'] != 'C':
            i['Value'] = int(i['Value'].replace(',',''))
        else:
            i.pop('Value')
        items.append(i)
    return items
# вывод минимальной, средней, максимальной Value
def two_first_query(collection):
    q = [{
        "$group": {
            "_id":'result',
            "max":{"$max": "$Value"},
            "min":{"$min": "$Value"},
            "avg":{"$avg": "$Value"}
        }
    }]
    result = []
    for stat in collection.aggregate(q):
        result.append(stat)
    # json_data = dumps(result, indent = 2, ensure_ascii=False)
    # with open(f'result_5_4_q2_1.json', 'w', encoding='utf-8') as f:
    #     f.write(json_data)
# вывод количества данных по представленным Industry_name_NZSIOC
def two_second_query(collection):
    q = [{
        "$group": {
            "_id":'$Industry_name_NZSIOC',
            "count":{"$sum": 1}
        }
    }, {
        "$sort": {
            "count":-1
        }
    }
    ]
    result = []
    for stat in collection.aggregate(q):
        result.append(stat)
    json_data = dumps(result, indent = 2, ensure_ascii=False)
    with open(f'result_5_4_q2_2.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
# вывод минимальной, средней, максимальной Value по Variable_category
def two_third_query(collection):
    q = [{
        "$group": {
            "_id":'$Variable_category',
            "max":{"$max": "$Value"},
            "min":{"$min": "$Value"},
            "avg":{"$avg": "$Value"}
        }
    }]
    result = []
    for stat in collection.aggregate(q):
        result.append(stat)
    json_data = dumps(result, indent = 2, ensure_ascii=False)
    with open(f'result_5_4_q2_3.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
# вывод максимальной Value при минимальном Industry_aggregation_NZSIOC
def two_fourth_qyery(collection):
    q = [{
        "$group": {
            "_id":'$Industry_aggregation_NZSIOC',
            "max_Value": {"$max":"$Value"}
            }
        }, {
            "$group" :{
                "_id":'result',
                "min_Industry_aggregation_NZSIOC" : {"$min": "$_Industry_aggregation_NZSIOC"},
                "max_Value": {"$max":"$max_Value"}
            }
    }]
    result = []
    for stat in collection.aggregate(q):
        result.append(stat)
    json_data = dumps(result, indent = 2, ensure_ascii=False)
    with open(f'result_5_4_q2_4.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
# произвольный запрос с $match, $group, $sort
def two_fifth_query(collection):
    q = [{
            "$match": {
                "Units": {"$in": ['Dollars (millions)', 'Dollars']}
            }
        },{
            "$group" : {
                "_id":'result',
                "max":{"$max": "$Value"},
                "min":{"$min": "$Value"},
                "avg":{"$avg": "$Value"}
            }
        },
        {
            "$sort": {
                "min": -1
            }
        }]
    result = []
    for stat in collection.aggregate(q):
        result.append(stat)
    json_data = dumps(result, indent = 2, ensure_ascii=False)
    with open(f'result_5_4_q2_5.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
# удалить из коллекции документы по предикату value

def three_first_query(collection):
    result = collection.delete_many({
        '$or' : [
            {'Value': {'$lt':10}},
            {'Value':{'$gt':100}}
        ]
    })
    print(result)
# увеличить возраст (age) всех документов на 1
def three_second_query(collection):
    result = collection.update_many({},{
        '$inc': {
            'Year': 1
        }
    })
    print(result)
# поднять Value на 7%
def three_third_query(collection):
    filter = {
        "Industry_aggregation_NZSIOC" : {"$in": ["Level 1", "Level 4"]}
    }
    update = {
            "$mul" : {
                'Value': 1.07
        }
    }
    result = collection.update_many(filter, update)
    print(result)
# data = get_from_csv('5_var_7/finans_year.csv')
# data_json = get_from_json('5_var_7/finans_year.json')
# insert_many(connect(), data)
first_query(connect())
second_query(connect())
third_qyery(connect())
fourth_qyery(connect())
# insert_many(connect(), data_json)
two_first_query(connect())
two_second_query(connect())
two_third_query(connect())
two_fourth_qyery(connect())
two_fifth_query(connect())
three_first_query(connect())
three_second_query(connect())
three_third_query(connect())
