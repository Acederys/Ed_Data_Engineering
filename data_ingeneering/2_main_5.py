# Найдите набор данных (csv, json), размер которого превышает 20-30Мб.
#
# Отберите для дальнейшей работы в нем 7-10 полей (пропишите это преобразование в коде).
# Для полей, представляющих числовые данные, рассчитайте характеристики:
# максимальное и минимальное значения, среднее арифметическое, сумму, стандартное отклонение.
# Для полей, представляющий текстовые данные (в виде меток некоторых категорий) рассчитайте частоту встречаемости.
# Сохраните полученные расчеты в json. Сохраните набор данных с помощью разных форматов: csv, json, msgpack, pkl.
# Сравните размеры полученных файлов.
import csv
import numpy as np

Warehouss = list()

with open('Warehouse_and_Retail_Sales.csv', 'r') as file:
    heading = next(file)
    data_Warehouse = csv.reader(file, delimiter=',', quotechar='|')

    for row in data_Warehouse:
        Warehouss.append(row)

YEAR = list()
# MONTH = dict()
# SUPPLIER = dict()
# ITEM = dict()
# CODE = dict()
# ITEM = dict()
# DESCRIPTION = dict()
# ITEM = dict()
# TYPE = dict()
# RETAIL = dict()
# SALES = dict()
# RETAIL = dict()
# TRANSFERS = dict()
# WAREHOUSE = dict()
# SALES = dict()

max_Ye = Warehouss[0][0]
min_Ye = Warehouss[0][0]
avr_Ye = 0
sum_Ye = 0
for i in range(0, len(Warehouss)):
    max_Ye = max(max_Ye, Warehouss[i][0])
    min_Ye = min(min_Ye, Warehouss[i][0])
    sum_Ye += int(Warehouss[i][0])
    avr_Ye = round(sum_Ye/len(Warehouss), 2)
    YEAR.append(i)
sigma = np.std(YEAR)
print(max_Ye)
print(min_Ye)
print(avr_Ye)
print(sum_Ye)
print(sigma)

