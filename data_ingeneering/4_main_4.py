# Дан набор файлов.
# В одних содержится информация о некоторых товарах, которые нужно сохранить в соответствующей таблице базы данных.
# В других (начинающихся с префикса upd) содержится информация об изменениях, которые могут задаваться разными командами:
# изменение цены, изменение остатков, снять/возврат продажи, удаление из каталога (таблицы).
# По одному товару могут быть несколько изменений, поэтому при создании таблицы необходимо предусмотреть поле-счетчик,
# которое инкрементируется каждый раз, когда происходит обновление строки. Все изменения необходимо производить,
# используя транзакции, проверяя изменения на корректность (например, цена или остатки после обновления не могут быть отрицательными)
#
# После записи всех данные и применения обновлений необходимо выполнить следующие запросы:
#
# вывести топ-10 самых обновляемых товаров
#
# проанализировать цены товаров, найдя (сумму, мин, макс, среднее) для каждой группы, а также количество товаров в группе
#
# проанализировать остатки товаров, найдя (сумму, мин, макс, среднее) для каждой группы товаров
#
# произвольный запрос
import msgpack
import sqlite3
import json
def parce_data(data_1):
    items = []
    with open(data_1, 'r', encoding='utf-8') as file:
        data = file.readlines()
        item = dict()
        for i in data:
            if i == '=====\n':
                item = dict()
                item['category'] = 'no'
                item['name'] = 'no'
                item['price'] = 'no'
                item['quantity'] = 'no'
                item['fromCity'] = 'no'
                item['isAvailable'] = 'no'
                item['views'] = 'no'
                items.append(item)
            else:
                i = i.strip()
                splitted = i.split('::')
                if splitted[0] in ['quantity','views']:
                    item[splitted[0]] = int(splitted[1])
                elif splitted[0] == 'price':
                    item[splitted[0]] = float(splitted[1])
                else:
                    item[splitted[0]] = splitted[1]
    clear_item = []
    for elem in items:
        if elem['name'] != 'no':
            clear_item.append(elem)
    return clear_item
def parce_data_mp(data_2):
    with open(data_2, 'rb') as mp_file:
        data_mp = msgpack.load(mp_file)
    for elem in data_mp:
        if elem['param'] == True:
            elem['param'] = 'True'
        else:
            elem['param'] = 'False'
    return data_mp

# подключаемся к базе данных
def connect_to_db(elem):
    connection = sqlite3.connect(elem)
    connection.row_factory = sqlite3.Row
    return connection

def insert_price(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO products (name, price, quantity, category, fromCity, isAvailable, views)
        VALUES(
        :name, :price, :quantity, :category, :fromCity, :isAvailable, :views
        )
    """, data)
    db.commit()

item_1 = parce_data('task_4_var_07_product_data.text')
item_2 = parce_data_mp('task_4_var_07_update_data.msgpack')
db = connect_to_db('4_1_db.db')
# insert_price(db, item_1)

def  update_priece(db, update_items):
    for item in update_items:
        if item['method'] == 'remove':
            pass
            # delete_be_name(db, [item['name']]
        elif item['method'] == 'price_percent':
            res = item['param'] * 100
            cursor = db.cursor()
            cursor.executemany("""
                UPDATE products SET price = price + ? WHERE name = ?
            """, [res, item['name']])
            cursor.executemany("""
                UPDATE products SET version = version + 1 WHERE name = ?
            """,  [item['name']])
            db.commit()
            # case ['quantity_add', 'quantity_sub']:
            #     quantity_add(db, item['name'], item['param'])
            # case 'available':
            #     available(db, item['name'], item['param'])
            # case 'price_abs':
            #     price_abs(db, item['name'], item['param'])


def delete_be_name(db, name):
    cursor = db.cursor()
    cursor.executemany("""
        DELETE FROM products WHERE name = ?
    """, [name])
    db.commit()

def update_price(db, name, percent):
    cursor = db.cursor()
    cursor.executemany("""
        UPDATE products SET price = price + (100*?) WHERE name = ?
    """, [percent, name])
    cursor.executemany("""
        UPDATE products SET version = version + 1 WHERE name = ?
    """, [name])
    db.commit()

def quantity_add(db, name, percent):
    cursor = db.cursor()
    cursor.executemany("""
        UPDATE products SET quantity = quantity + ? WHERE name = ?
    """, [percent, name])
    cursor.executemany("""
        UPDATE productsSET version = version + 1 WHERE name = ?
    """, [name])
    db.commit()

def available(db, name, percent):
    cursor = db.cursor()
    cursor.executemany("""
        UPDATE products SET isAvailable = ? WHERE name = ?
    """, [percent, name])
    cursor.executemany("""
        UPDATE productsSET version = version + 1 WHERE name = ?
    """, [name])
    db.commit()

def price_abs(db, name, percent):
    cursor = db.cursor()
    cursor.executemany("""
        UPDATE products SET price = price + ? WHERE name = ?
    """, [percent, name])
    cursor.executemany("""
        UPDATE productsSET version = version + 1 WHERE name = ?
    """, [name])
    db.commit()
update_priece(db, item_2)
