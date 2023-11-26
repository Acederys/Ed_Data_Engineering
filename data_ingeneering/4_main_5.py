# Самостоятельно выбрать предметную область.
# Подобрать пару наборов данных разных форматов.
# Создать базу данных минимум на три таблицы.
# Заполнение данных осуществляем из файлов.
# Реализовать выполнение 6-7 запросов к базе данных с выводом результатов в json. Среди них могут быть:
#
# выборка с простым условием + сортировка + ограничение количество
#
# подсчет объектов по условию, а также другие функции агрегации
#
# группировка
#
# обновление данных
#
# В решении необходимо указать:
#
# название и описание предметной области (осмысленное)
#
# SQL для создания таблиц
#
# файлы исходных данных (можно обрезать до такого размера, чтобы влезли в GitHub)
#
# скрипт для инициализации базы данных (создание таблиц)
#
# скрипт для загрузки данных из файлов в базу данных
#
# файл базы данных
#
# скрипт с выполнением запросов к базе данных  
import csv
import json
import pandas as pd
import sqlite3
# загрузжаем данне
with open('apartment.csv') as file:
    data_csv = csv.reader(file)
    next(data_csv)
    data = []
    for i in data_csv:
        # print(i)
        item = {
            'ListYear': int(i[0]),
            'Address': i[2],
            'SaleAmount': float(i[4]),
            'PropertyType': i[5]
        }
        data.append(item)
item_1 = data.copy()
# подключаемся к БД
def connect_to_db(elem):
    connection = sqlite3.connect(elem)
    connection.row_factory = sqlite3.Row
    return connection
db = connect_to_db('4_5_db.db')

def insert_price(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO apartament (ListYear, Address, SaleAmount, PropertyType)
        VALUES(
        :ListYear, :Address, :SaleAmount, :PropertyType
        )
    """, data)
    db.commit()

# insert_price(db, item_1)

df = pd.read_json('AssessedValue.json')
item_2 = df.to_dict('records')
def insert_AssessedValue(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO AsessedValue (id_AsessedValue, Address, AssessedValue)
        VALUES(
            (SELECT id FROM apartament WHERE Address = :Address),
        :Address, :AssessedValue
        )
    """, data)
    db.commit()

# insert_AssessedValue(db, item_2)

df = pd.read_csv('town.csv')
item_3 = df.to_dict('records')
print(len(item_3))
def insert_town(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO town (id_town, Town, Address)
        VALUES(
            (SELECT id FROM apartament WHERE Address = :Address),
        :Town, :Address
        )
    """, data)
    db.commit()

# insert_town(db, item_3)

def first_query(db, limit):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT *
        FROM apartament
        WHERE SaleAmount > 10000
        ORDER BY PropertyType DESC
        LIMIT ?
        """,[limit])
    items = []
    for row in result.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    # with open(f'SaleAmount_10000.json', 'w', encoding='utf-8') as file_1:
    #     file_1.write(json.dumps(items))
first_query(db, 100)


# подсчет объектов по условию

def second_query(db, name):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT *
        FROM town
        WHERE id_town = (SELECT id FROM apartament WHERE PropertyType = ?)
        """, [name])
    items = []
    for row in result.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    # with open(f'Residential.json', 'w', encoding='utf-8') as file_1:
    #     file_1.write(json.dumps(items))

second_query(db, 'Residential')

def therr_query(db, name):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT *
        FROM apartament
        WHERE id = (SELECT id_town FROM town WHERE Town = ?)
        """, [name])
    items = []
    for row in result.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    # with open(f'Ansonia.json', 'w', encoding='utf-8') as file_1:
    #     file_1.write(json.dumps(items))
therr_query(db, 'Ansonia')


def foir_query(db, name):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT *
        FROM AsessedValue
        WHERE AssessedValue > 10000
        LIMIT ?
        """, [name])
    items = []
    for row in result.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    # with open(f'AssessedValue_10000.json', 'w', encoding='utf-8') as file_1:
    #     file_1.write(json.dumps(items))

foir_query(db, 10)

def five_query(db, name):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT 
            AVG(AssessedValue) as avg_AssessedValue,
            *
        FROM AsessedValue
        WHERE id_AsessedValue = (SELECT id FROM town WHERE Town = ?)
        """, [name])
    items = []
    for row in result.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    print(items)
    # with open(f'avg_AssessedValue.json', 'w', encoding='utf-8') as file_1:
    #     file_1.write(json.dumps(items))

five_query(db, 'Ansonia')

def six_query(db, name):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT *
        FROM apartament
        WHERE id = (SELECT id_AsessedValue FROM AsessedValue  WHERE AssessedValue < ?)
        """, [name])
    items = []
    for row in result.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    # with open(f'AssessedValue_9999999.json', 'w', encoding='utf-8') as file_1:
    #     file_1.write(json.dumps(items))

six_query(db, 9999999)
