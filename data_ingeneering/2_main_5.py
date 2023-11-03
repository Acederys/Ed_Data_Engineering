# Найдите набор данных (csv, json), размер которого превышает 20-30Мб.
#
# Отберите для дальнейшей работы в нем 7-10 полей (пропишите это преобразование в коде).
# Для полей, представляющих числовые данные, рассчитайте характеристики:
# максимальное и минимальное значения, среднее арифметическое, сумму, стандартное отклонение.
# Для полей, представляющий текстовые данные (в виде меток некоторых категорий) рассчитайте частоту встречаемости.
# Сохраните полученные расчеты в json. Сохраните набор данных с помощью разных форматов: csv, json, msgpack, pkl.
# Сравните размеры полученных файлов.
import csv
import json

import numpy as np
import msgpack
import pickle
import os

Warehouss = list()

with open('Warehouse_and_Retail_Sales.csv', 'r', newline="") as file:
    heading = next(file)
    data_Warehouse = csv.reader(file)

    for row in data_Warehouse:
        Warehouss.append(row)

# числовая часть
YEAR = list()
MONTH = list()
SUPPLIER = list()
ITEM_CODE = list()
ITEM_DESCRIPTION = list()
ITEM_TYPE = list()
RETAIL_SALES = list()
RETAIL_TRANSFERS = list()
WAREHOUSE_SALES = list()

size = len(Warehouss)

full_item = list()
def func_math(item):
    max_it = float(item[0])
    min_it = float(item[0])
    avr_it = 0.0
    sum_it = 0.0
    all_elem = list()
    for i in item:
        max_it = max(max_it, float(i))
        min_it = min(min_it, float(i))
        sum_it += float(i)
        avr_it = round(sum_it/size)
        all_elem.append(float(i))
    sigma = np.std(all_elem)
    elem = {
        'max_it': max_it,
        'min_it': min_it,
        'sum_it': sum_it,
        'avr_it': avr_it,
        'sigma': sigma
    }
    return elem

full_coll = list()
for i in range(0, len(Warehouss)):
    YEAR.append(Warehouss[i][0])
    MONTH.append(Warehouss[i][1])
    SUPPLIER.append(Warehouss[i][2])
    ITEM_CODE.append(Warehouss[i][3])
    ITEM_DESCRIPTION.append(Warehouss[i][4])
    ITEM_TYPE.append(Warehouss[i][5])
    RETAIL_SALES.append(Warehouss[i][6])
    RETAIL_TRANSFERS.append(Warehouss[i][7])
    WAREHOUSE_SALES.append(Warehouss[i][8])
def replace_item(list_elem):
    for item in range(0, len(list_elem)):
        if list_elem[item]=='BC' or list_elem[item]=='WC' or list_elem[item] == '':
            list_elem[item] = 0
    return list_elem
YEAR = replace_item(YEAR)
RETAIL_SALES = replace_item(RETAIL_SALES)
WAREHOUSE_SALES = replace_item(WAREHOUSE_SALES)

full_YEAR = func_math(YEAR)
full_MONTH = func_math(MONTH)
full_RETAIL_SALES = func_math(RETAIL_SALES)
full_RETAIL_TRANSFERS = func_math(RETAIL_TRANSFERS)
full_WAREHOUSE_SALES = func_math(WAREHOUSE_SALES)

# строковая часть

def func_repeat(elem):
    dict_all = dict()
    for i in sorted(elem):
        if i in dict_all:
            dict_all[i] += 1
        else:
            dict_all[i] = 1
    dict_all = dict(sorted(dict_all.items(), reverse=True, key=lambda item: item[1]))
    return dict_all
full_SUPPLIER = func_repeat(SUPPLIER)
# Данный столбец является кодом товала и записан вместе с латинскими буквами
full_ITEM_CODE = func_repeat(ITEM_CODE)
full_ITEM_DESCRIPTION = func_repeat(ITEM_DESCRIPTION)
full_ITEM_TYPE = func_repeat(ITEM_TYPE)


data_collum = {
    'YEAR' : full_YEAR,
    'MONTH': full_MONTH,
    'SUPPLIER' : full_SUPPLIER,
    'ITEM_CODE': full_ITEM_CODE,
    'ITEM_DESCRIPTION': full_ITEM_DESCRIPTION,
    'ITEM_TYPE': full_ITEM_TYPE,
    'RETAIL_SALES': full_RETAIL_SALES,
    'RETAIL_TRANSFERS': full_RETAIL_TRANSFERS,
    'WAREHOUSE_SALES': full_WAREHOUSE_SALES
}

with open(r'result_2_5.json', 'w') as rezults:
    rezults.write(json.dumps(data_collum))

with open(r'Warehouse_and_Retail_Sales.json', 'w') as file:
    file.write(json.dumps(Warehouss))

with open(r'Warehouse_and_Retail_Sales.msgpack', 'wb') as file:
    file.write(msgpack.dumps(Warehouss))

with open(r'Warehouse_and_Retail_Sales.pickle', 'wb') as file:
    file.write(pickle.dumps(Warehouss))

print(f'result csv: {os.path.getsize("Warehouse_and_Retail_Sales.csv")}')
print(f'result json: {os.path.getsize("Warehouse_and_Retail_Sales.json")}')
print(f'result msgpack: {os.path.getsize("Warehouse_and_Retail_Sales.msgpack")}')
print(f'result pickle: {os.path.getsize("Warehouse_and_Retail_Sales.pickle")}')
