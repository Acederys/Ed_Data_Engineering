# Дан файл с некоторыми данными. Формат файла – произвольный.
# Спроектируйте на его основе и создайте таблицу в базе данных (SQLite).
# Считайте данные из файла и запишите их в созданную таблицу.
# Реализуйте и выполните следующие запросы:
#
# вывод первых (VAR+10) отсортированных по произвольному числовому полю строк из таблицы в файл формата json;
#
# вывод (сумму, мин, макс, среднее) по произвольному числовому полю;
#
# вывод частоты встречаемости для категориального поля;
#
# вывод первых (VAR+10) отфильтрованных по произвольному предикату отсортированных по произвольному числовому полю строк из таблицы в файл формате json.
import json
import sqlite3
# считываем данные с файла
def parce_data(data):
    items = []
    with open(data, 'r', encoding='utf-8') as file:
        data_js = json.load(file)
        for i in data_js:
            items.append(i)
    return items
# подключаемся к базе данных
def connect_to_db(elem):
    connection = sqlite3.connect(elem)
    connection.row_factory = sqlite3.Row
    return connection
# записываем данные в бд
def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO biblio (title, author, genre, pages, published_year, isbn, rating, views)
        VALUES(
        :title, :author, :genre, :pages, :published_year, :isbn, :rating, :views
        )
    
    """, data)
    db.commit()
# вывод первых (VAR+10) отсортированных по произвольному числовому полю строк из таблицы в файл формата json;
def get_top_by_views(db, limit):
    cursor = db.cursor()
    result = cursor.execute("SELECT * FROM biblio ORDER BY pages DESC LIMIT ?", [limit])
    items = []
    for row in result.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items
    # with open(f'result_4_1_order_pages.json', 'w', encoding='utf-8') as file:
    #     file.write(json.dumps(items, ensure_ascii=False))
# вывод (сумму, мин, макс, среднее) по произвольному числовому полю
def min_max(db):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT 
            SUM(views) as sum,
            AVG(views) as avg,
            MIN(views) as min,
            MAX(views) as max
        FROM biblio
        """)
    print(dict(result.fetchone()))
    cursor.close()
    return []
# вывод частоты встречаемости для категориального поля;
def get_occuerrence(db):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT 
            COUNT(*) as count,
            author as author
            FROM biblio
            GROUP BY author
        """)
    print([dict(row) for row in result.fetchall()])
    cursor.close()
    return []
def get_sort_rating(db,min_rating, limit):
    cursor = db.cursor()
    result = cursor.execute("""
        SELECT * 
        FROM biblio 
        WHERE rating > ?
        ORDER BY rating DESC 
        LIMIT ?
        """, [min_rating, limit])
    items = []
    for row in result.fetchall():
        items.append(dict(row))
    cursor.close()
    return items
    # with open(f'result_4_1_filter_rating.json', 'w', encoding='utf-8') as file:
    #     file.write(json.dumps(items, ensure_ascii=False))
# вывод первых (VAR+10) отфильтрованных по произвольному предикату отсортированных по произвольному числовому полю строк из таблицы в файл формате json.

item = parce_data('task_1_var_07_item.json')
db = connect_to_db('4_1_db.db')
# insert_data(db, item)
get_top_by_views(db, 17)
min_max(db)
get_occuerrence(db)
get_sort_rating(db, 4.0, 17)
