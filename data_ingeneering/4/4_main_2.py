# Дан файл с некоторыми данными.
# Формат файла – произвольный.
# Данные некоторым образом связаны с теми, что были добавлены в первом задании.
# Необходимо проанализировать и установить связь между таблицами.
# Создать таблицу и наполнить ее прочитанными данными из файла.
# Реализовать и выполнить 3 запроса, где используется связь между таблицами.
# считываем данные с файла
import sqlite3
import json
def parce_data(data):
    items = []
    with open(data, 'r', encoding='utf-8') as file:
        data = file.readlines()
        item = dict()
        for i in data:
            if i == '=====\n':
                items.append(item)
                item = dict()
            else:
                i = i.strip()
                splitted = i.split('::')
                if splitted[0] == 'price':
                    item[splitted[0]] = int(splitted[1])
                else:
                    item[splitted[0]] = splitted[1]
    return items
# подключаемся к базе данных
def connect_to_db(elem):
    connection = sqlite3.connect(elem)
    connection.row_factory = sqlite3.Row
    return connection
def insert_price(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO book (biblio_id, title, price, place, date)
        VALUES(
            (SELECT id FROM biblio WHERE title = :title),
        :title, :price, :place, :date
        )
    """, data)
    db.commit()

def first_query(db, name):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT *
        FROM book
        WHERE biblio_id = (SELECT id FROM biblio WHERE author = ?)
        """, [name])
    items = dict(result.fetchone())
    with open(f'result_4_2_1_order_pages.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(items, ensure_ascii=False))
    cursor.close()
    return []

def second_query(db, name):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT 
            AVG(price) as avg_price
        FROM book
        WHERE biblio_id = (SELECT id FROM biblio WHERE author = ?)
        """, [name])
    items = []
    for row in result.fetchall():
        item = dict(row)
        items.append(item)
    with open(f'result_4_2_2_order_pages.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(items, ensure_ascii=False))
    cursor.close()

def third_query(db):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT 
            author,
            (SELECT COUNT(*) FROM book WHERE id = biblio_id) as title
        FROM biblio
        ORDER BY title
        LIMIT 10
        """)
    items = []
    for row in result.fetchall():
        item = dict(row)
        items.append(item)
    with open(f'result_4_2_3_order_pages.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(items, ensure_ascii=False))
    cursor.close()
item = parce_data('task_2_var_07_subitem.text')
db = connect_to_db('4_1_db.db')
# insert_price(db, item)
first_query(db, 'Дж. Р. Р. Толкин')
second_query(db, 'Дж. Р. Р. Толкин')
third_query(db)
