# Дано два файла разных форматов.
# Необходимо проанализировать их структуру и выделить общие хранимые данные.
# Необходимо создать таблицу для хранения данных в базе данных.
# Произведите запись данных из файлов разных форматов в одну таблицу.
# Реализуйте и выполните следующие запросы:
#
# вывод первых (VAR+10) отсортированных по произвольному числовому полю строк из таблицы в файл формата json;
#
# вывод (сумму, мин, макс, среднее) по произвольному числовому полю;
#
# вывод частоты встречаемости для категориального поля;
#
# вывод первых (VAR+15) отфильтрованных по произвольному предикату отсортированных по произвольному числовому полю строк из таблицы в файл формате json.
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
                items.append(item)
                item = dict()
            else:
                i = i.strip()
                splitted = i.split('::')
                if splitted[0] == 'duration_ms' or splitted[0] == 'year':
                    item[splitted[0]] = int(splitted[1])
                elif splitted[0] == 'tempo':
                    item[splitted[0]] = float(splitted[1])
                elif splitted[0] == 'explicit' or splitted[0] == 'loudness':
                    continue
                else:
                    item[splitted[0]] = splitted[1]
    return items
def parce_data_mp(data_2):
    with open(data_2, 'rb') as mp_file:
        data_mp = msgpack.load(mp_file)
        for item in data_mp:
            item.pop('speechiness')
            item.pop('mode')
            item.pop('acousticness')
    return data_mp

# подключаемся к базе данных
def connect_to_db(elem):
    connection = sqlite3.connect(elem)
    connection.row_factory = sqlite3.Row
    return connection

item_1 = parce_data('task_3_var_07_part_1.text')
item_2 = parce_data_mp('task_3_var_07_part_2.msgpack')
db = connect_to_db('4_1_db.db')
items = item_1 + item_2

def insert_price(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO music (artist, song, duration_ms, year, tempo, genre, instrumentalness)
        VALUES(
        :artist, :song, :duration_ms, :year, :tempo, :genre, :instrumentalness
        )
    """, data)
    db.commit()

# insert_price(db, items)

# вывод первых (VAR+10) отсортированных по произвольному числовому полю строк из таблицы в файл формата json;
def get_top_by_views(db, limit):
    cursor = db.cursor()
    result = cursor.execute("SELECT * FROM music ORDER BY artist DESC LIMIT ?", [limit])
    items = []
    for row in result.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items
    # with open(f'result_4_3_order_artist.json', 'w', encoding='utf-8') as file:
    #     file.write(json.dumps(items, ensure_ascii=False))

get_top_by_views(db, 17)
# вывод (сумму, мин, макс, среднее) по произвольному числовому полю
def min_max(db):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT 
            SUM(duration_ms) as sum,
            AVG(duration_ms) as avg,
            MIN(duration_ms) as min,
            MAX(duration_ms) as max
        FROM music
        """)
    print(dict(result.fetchone()))
    cursor.close()
    return []

min_max(db)


# вывод частоты встречаемости для категориального поля;
def get_occuerrence(db):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT 
            COUNT(*) as count,
            artist as artist
            FROM music
            GROUP BY artist
        """)
    print(dict(result.fetchall()))
    cursor.close()
    return []
get_occuerrence(db)

def get_sort_year(db,min_rating, limit):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT * 
        FROM music 
        WHERE year > ?
        ORDER BY year DESC 
        LIMIT ?
        """, [min_rating, limit])
    items = []
    for row in result.fetchall():
        items.append(dict(row))
    cursor.close()
    # return items
    with open(f'result_4_3_filter_year.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(items, ensure_ascii=False))
# вывод первых (VAR+10) отфильтрованных по произвольному предикату отсортированных по произвольному числовому полю строк из таблицы в файл формате json.
get_sort_year(db, 2010, 17)
