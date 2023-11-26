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

def parce_data(data_1):
    items = []
    with open(data_1, 'r', encoding='utf-8') as file:
        data = file.readlines()
        item = dict()
        for i in data:
            if i == '=====\n':
                item = dict()
                item['category'] = 'no'
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
    clear_items = []
    for i in items:
        if i.get('name', False) != False:
            clear_items.append(i)
    return clear_items
item_1 = parce_data('task_4_var_07_product_data.text')
# print(len(item_1))
# print(item_1)

# подключаемся к базе данных
def connect_to_db(elem):
    connection = sqlite3.connect(elem)
    connection.row_factory = sqlite3.Row
    return connection
db = connect_to_db('4_1_db.db')

def insert_price(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO products (name, price, quantity, category, fromCity, isAvailable, views)
        VALUES(
        :name, :price, :quantity, :category, :fromCity, :isAvailable, :views
        )
    """, data)
    db.commit()

# insert_price(db, item_1)

def delete_by_name(db, name):
    cursor = db.cursor()
    cursor.execute('DELETE FROM products WHERE name = ?', [name])
    db.commit()
def update_price_by_precent(db, name, precent):
    cursor = db.cursor()
    cursor.execute('UPDATE products SET price = ROUND((price * (1 + ?)), 2) WHERE name = ?', [precent, name])
    cursor.execute('UPDATE products SET version = version +1 WHERE  name = ?', [name])
    db.commit()
def quantity_add(db, name, quantity):
    cursor = db.cursor()
    res = cursor.execute('UPDATE products SET quantity = (quantity + ?) WHERE (name = ?) AND ((quantity + ?)> 0)', [quantity, name, quantity])
    if res.rowcount > 0:
        cursor.execute('UPDATE products SET version = version +1 WHERE  name = ?', [name])
        db.commit()
def price_abs(db, name, value):
    cursor = db.cursor()
    res = cursor.execute('UPDATE products SET price = (price + ?) WHERE (name = ?) AND ((price + ?)> 0)', [value, name, value])
    if res.rowcount > 0:
        cursor.execute('UPDATE products SET version = version +1 WHERE  name = ?', [name])
        db.commit()
def available(db, name, value):
    cursor = db.cursor()
    res = cursor.execute('UPDATE products SET isAvailable = ? WHERE (name = ?)', [value, name])
    cursor.execute('UPDATE products SET version = version +1 WHERE  name = ?', [name])
    db.commit()


def parce_data_mp(data_2):
    with open(data_2, 'rb') as mp_file:
        data_mp = msgpack.load(mp_file)
    for elem in data_mp:
        if elem['method'] == 'available' and elem['param'] == True:
            elem['param'] = 'True'
        elif elem['method'] == 'available' and elem['param'] == False:
            elem['param'] = 'False'
    return data_mp
item_2 = parce_data_mp('task_4_var_07_update_data.msgpack')

def hungle_update(db, update_items):
    for item in update_items:
        match item['method']:
            case 'remove':
                print(f'Удалить {item["name"]}')
                delete_by_name(db, item["name"])
            case 'price_percent':
                print(f"Изменить на процент {item['name']} {item['param']}")
                update_price_by_precent(db, item['name'], item['param'])
            case 'price_abs':
                print(f"Изменение цены {item['name']} {item['param']}")
                price_abs(db, item['name'], item['param'])
            case 'available':
                print(f"Изменение доступности {item['name']} {item['param']}")
                price_abs(db, item['name'], item['param'])
            case 'quantity_add':
                print(f"Изменение количества {item['name']} {item['param']}")
                quantity_add(db, item['name'], item['param'])
            case 'quantity_sub':
                print(f"Изменение количества {item['name']} {item['param']}")
                price_abs(db, item['name'], item['param'])


# hungle_update(db, item_2)

#вывести топ-10 самых обновляемых товаров

def first_query(db, limit):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT *
        FROM products
        ORDER BY version DESC
        LIMIT ?
        """,[limit])
    items = []
    for row in result.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    print(items)
first_query(db, 10)
# проанализировать цены товаров, найдя (сумму, мин, макс, среднее) для каждой группы, а также количество товаров в группе
def min_max(db):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT
            SUM(price) as sum_price,
            AVG(price) as avg_price,
            MIN(price) as min_price,
            MAX(price) as max_price,
            SUM(quantity) as sum_quantity,
            AVG(quantity) as avg_quantity,
            MIN(quantity) as min_quantity,
            MAX(quantity) as max_quantity,
            SUM(views) as sum_views,
            AVG(views) as avg_views,
            MIN(views) as min_views,
            MAX(views) as max_views
        FROM products
        """)
    print(dict(result.fetchone()))
    cursor.close()
    return []

min_max(db)

# проанализировать остатки товаров, найдя (сумму, мин, макс, среднее) для каждой группы товаров
def anasis_quality(db):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT category, AVG(quantity) as avg_price
        FROM products
        GROUP BY category
        """)
    print(dict(result.fetchall()))
    cursor.close()
    return []

anasis_quality(db)

# произвольный запрос
def second_query(db):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT
            COUNT(*) as count,
            fromCity as fromCity
            FROM products
            GROUP BY fromCity
        """)
    items = []
    for row in result.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    print(items)

second_query(db)
