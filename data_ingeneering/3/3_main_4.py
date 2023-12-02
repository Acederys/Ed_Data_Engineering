# Исследовать структуру xml-файлов, чтобы произвести парсинг всех данных.
# В каждом файле содержится информация об одном или нескольких объектах из случайной предметной области.
# Перечень всех характеристик объекта может меняться
# (у отдельного объекта могут отсутствовать некоторые характеристики).
# Полученные данные собрать и записать в json.
# Выполните также ряд операций с данными:
#
# отсортируйте значения по одному из доступных полей
#
# выполните фильтрацию по другому полю (запишите результат отдельно)
#
# для одного выбранного числового поля посчитайте статистические характеристики (сумма, мин/макс, среднее и т.д.)
#
# для одного текстового поля посчитайте частоту меток
from bs4 import BeautifulSoup
from lxml import etree
import xml
import json
import pandas as pd
urls = list()
for i in range(1, 101):
    urls.append(f'3_4_var_7/{i}.xml')
items = list()
# with open('3_4_var_7/60.xml', 'r', encoding='utf-8') as file:
#      data = file.read()
#      soup = BeautifulSoup(data, 'xml')
#      products = soup.find_all('clothing')
#      print(products)
for url in urls:
    with open(url, 'r', encoding='utf-8') as file:
        data = file.read()
        soup = BeautifulSoup(data, 'xml')
        products = soup.find_all('clothing')
        for product in products:
            item = {
                'id': int(soup.find('id').get_text().strip()),
                'name': soup.find('name').get_text().strip(),
                'category': soup.find('category').get_text().strip(),
                'size': soup.find('size').get_text().strip(),
                'color': soup.find('color').get_text().strip(),
                'material': soup.find('material').get_text().strip(),
                'price': int(soup.find('price').get_text().strip()),
                'rating': float(soup.find('rating').get_text().strip()),
                'new': soup.find('new').get_text().strip(),
                'reviews': int(soup.find('reviews').get_text().strip()),
                'exclusive': soup.find('exclusive').get_text().strip(),
                'sporty': soup.find('sporty').get_text().strip(),
            }
            items.append(item)
for item in items:
    if item['category'] == '':
        item.pop('category')
    if item['size'] == '':
        item.pop('size')
    if item['color'] == '':
        item.pop('color')
    if item['material'] == '':
        item.pop('material')
    if item['price'] == '':
        item.pop('price')
    if item['rating'] == '':
        item.pop('rating')
    if item['new'] == '':
        item.pop('new')
    if item['reviews'] == '':
        item.pop('reviews')
    if item['exclusive'] == '':
        item.pop('exclusive')
    if item['sporty'] == '':
        item.pop('sporty')
with open(r'result_3_4.json', 'w', encoding='utf-8') as rezults:
    rezults.write(json.dumps(items, ensure_ascii=False))
with open('result_3_4.json', 'r', encoding='utf-8') as file:
    files = json.load(file)
    files_sort = sorted(files, key=lambda x: x['id'], reverse=True)
with open(r'result_3_4_sort.json', 'w', encoding='utf-8') as rezults_sort:
    rezults_sort.write(json.dumps(files_sort, ensure_ascii=False))
items_caption = dict()
for i in files_sort:
    if i.get('material', False) != False:
        if i['material'] in items_caption:
            items_caption[i['material']]+=1
        else:
            items_caption[i['material']]=1
print(items_caption)
item_exclusive = list()
for item in files_sort:
    if item.get('exclusive', False) != False:
        if item['exclusive'] != 'no':
            item_exclusive.append(item)
with open(r'result_3_4_filter.json', 'w', encoding='utf-8') as rezults_filter:
    rezults_filter.write(json.dumps(item_exclusive, ensure_ascii=False))

df = pd.read_json('result_3_4.json')
df_price = df['price'].describe()
print(df_price)


