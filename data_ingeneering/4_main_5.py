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
import pandas as pd
import sqlite3
df = pd.read_csv('df_2009.csv')
clear_df = df.drop_duplicates(subset=['Address'])
clear_df.rename(columns = {'List Year':' ListYear', 'Date Recorded':'DateRecorded', 'Assessed Value':'AssessedValue', 'Sale Amount':'SaleAmount', 'Property Type': 'PropertyType', 'Residential Type':'ResidentialType'}, inplace = True )
clear_df.insert(loc= len(clear_df.columns) , column='version', value=0)

#подключаемся к базе данных
def connect_to_db(elem):
    connection = sqlite3.connect(elem)
    connection.row_factory = sqlite3.Row
    return connection

# def insert_price(db, data):
#     cursor = db.cursor()
#     cursor.executemany("""
#         INSERT INTO apartament (ListYear, DateRecorded, Town, Address, AssessedValue, SaleAmount, PropertyType, ResidentialType, version)
#         VALUES(
#         :ListYear, :DateRecorded, :Town, :Address, :AssessedValue, :SaleAmount, :PropertyType, :ResidentialType, :version
#         )
#     """, data)
#     db.commit()
db = connect_to_db('4_1_db.db')
# insert_price(db, clear_df)
df.to_sql("apartament", con=con, if_exists="append", index=False)
# pd.read_sql('''
#     SELECT *
#     FROM user
# ''', con)
