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
                item['version'] = 0
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
        if elem['method'] == 'available' and elem['param'] == True:
            elem['param'] = 'True'
        elif elem['method'] == 'available' and elem['param'] == False:
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
        INSERT INTO products_1 (name, price, quantity, category, fromCity, isAvailable, views, version)
        VALUES(
        :name, :price, :quantity, :category, :fromCity, :isAvailable, :views, :version
        )
    """, data)
    db.commit()

item_1 = parce_data('task_4_var_07_product_data.text')
item_2 = parce_data_mp('task_4_var_07_update_data.msgpack')
db = connect_to_db('4_1_db.db')
# insert_price(db, item_1)

# def  update_priece(db, update_items):
#     for item in update_items:
#         if item['method'] == 'remove':
#             pass
#             # delete_be_name(db, [item['name']])
#         elif item['method'] == 'price_percent':
#             name = item['name']
#             cursor = db.cursor()
#             result = cursor.executemany("""
#                 SELECT price
#                 FROM products_1
#                 WHERE name = ?
#                 """,name)
#             print(result.fetchone())
#             items = []
#             for row in result.fetchall():
#                 items.append(dict(row))
#             cursor.close()
            # print(items)
            # update_price(db, item['name'], item['param'])
            # update_version(db, item['name'])
        # elif item['method'] == ['quantity_add', 'quantity_sub']:
        #     quantity_add(db, item['name'], item['param'])
        #     update_version(db, item['name'])
        # elif item['method'] == 'available':
        #     available(db, item['name'], item['param'])
        #     update_version(db, item['name'])
        # elif item['method'] == 'price_abs':
        #     price_abs(db, item['name'], item['param'])
        #     update_version(db, item['name'])


def delete_be_name(db, name):
    cursor = db.cursor()
    cursor.executemany("""
        DELETE FROM products_1 WHERE name = ?
    """, [name])
    db.commit()

def update_price(db, name, percent):
    cursor = db.cursor()
    sql_update_query = """UPDATE products_1 SET price = ? WHERE name = ?"""
    data = (percent,name)
    cursor.execute(sql_update_query, data)
    db.commit()
    cursor.close()

def quantity_add(db, name, percent):
    cursor = db.cursor()
    sql_update_query = """UPDATE products_1 SET quantity = quantity + ? WHERE name = ?"""
    data = (percent,name)
    cursor.execute(sql_update_query, data)
    db.commit()
    cursor.close()

def available(db, name, percent):
    cursor = db.cursor()
    sql_update_query = """UPDATE products_1 SET isAvailable =  ? WHERE name = ?"""
    data = (percent,name)
    cursor.execute(sql_update_query, data)
    db.commit()
    cursor.close()

def price_abs(db, name, percent):
    cursor = db.cursor()
    sql_update_query = """UPDATE products_1 SET price = price + ? WHERE name = ?"""
    data = (percent,name)
    cursor.execute(sql_update_query, data)
    db.commit()
    cursor.close()
def update_version(db, name):
    cursor = db.cursor()
    sql_update_query = """UPDATE products_1 SET version = version+? WHERE name = ?"""
    data = (1, name)
    cursor.execute(sql_update_query, data)
    db.commit()
    cursor.close()

# update_priece(db, item_2)
# вывести топ-10 самых обновляемых товаров
def downloads_db(db):
    cursor = db.cursor()
    result = cursor.execute("""
    SELECT *
        FROM products_1
    """,)
    data = []
    for row in result.fetchall():
        elem = dict(row)
        data.append(elem)
    cursor.close()
    return data
def third_query(db, update_items, data):
    products = dict()
    data_json = data
    for elem in data_json:
        products[elem['name']] = elem
    print(data)
    # Ищем элемент файле с ценами
    for elem in update_items:
        # соединяем имена из двух словарей
        item = products[elem['name']]
        if elem['method'] == 'price_abs':
            res = item['price'] + elem['param']
            if res > 0:
                price_abs(db, item['name'], elem['param'])
                update_version(db, item['name'])
        elif elem['method'] == 'price_percent':
            res = item['price'] + (item['price']*elem['param'])
            if res > 0:
                update_price(db, item['name'], res)
                update_version(db, item['name'])
        elif elem['method'] == 'quantity_add':
            res = item['quantity'] + elem['param']
            if res > 0:
                quantity_add(db, item['name'], elem['param'])
                update_version(db, item['name'])
        elif elem['method'] == 'available':
            available(db, item['name'], elem['param'])
            update_version(db, item['name'])
        elif elem['method'] == 'remove':
            delete_be_name(db, [item['name']])
# 'beautiful baby shampoo'
    # for item in update_items:
    #     if item['method'] == 'price_abs':
    #         print([item['name']])

            # k = item[elements['name']]
            # print(k)
                # res = elem['price'] + item['param']
                # if res > 0:
                #     print(res,item['name'], elem['price'], item['param'])
            #         sql_update_query = """UPDATE products_1 SET price = price + ? WHERE name = ?"""
            #         data = (item['param'],[item['name']])
            #         cursor.execute(sql_update_query, data)
            #         db.commit()
            # cursor.close()

    # cursor = db.cursor()
    # result = cursor.execute("""
    #     SELECT *
    #     FROM products_1
    #     ORDER BY price DESC
    #     """)
    # items = []
    # for row in result.fetchall():
    # cursor.close()
    # print(items)
data = downloads_db(db)
print(len(data))
third_query(db, item_2, data)
