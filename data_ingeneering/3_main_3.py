# Исследовать структуру xml-файлов, чтобы произвести парсинг всех данных.
# В каждом файле содержится информация об одном объекте из случайной предметной области.
# Полученные данные собрать и записать в json. Выполните также ряд операций с данными:
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
for i in range(1, 501):
    urls.append(f'3_3_var_7/{i}.xml')
items = list()
for url in urls:
    with open(url, 'r', encoding='utf-8') as file:
        data = file.read()
        soup = BeautifulSoup(data, 'xml')
        item = {
            'name': soup.find('name').get_text().strip(),
            'constellation': soup.find('constellation').get_text().strip(),
            'spectral-class': soup.find('spectral-class').get_text().strip(),
            'radius': int(soup.find('radius').get_text()),
            'rotation': soup.find('rotation').get_text().strip(),
            'age': soup.find('age').get_text().strip(),
            'distance': soup.find('distance').get_text().strip(),
            'absolute-magnitude': soup.find('absolute-magnitude').get_text().strip()
        }
        items.append(item)
with open(r'result_3_3.json', 'w', encoding='utf-8') as results:
    results.write(json.dumps(items, ensure_ascii=False))

with open('result_3_3.json', 'r', encoding='utf-8') as file_json:
    files_json = json.load(file_json)
    files_json = sorted(files_json, key=lambda x: x['distance'], reverse=False)

with open(r'result_3_3_sort.json', 'w', encoding='utf-8') as file_sort:
    file_sort.write(json.dumps(files_json, ensure_ascii=False))

items_constellation = dict()
for i in files_json:
    if i['constellation'] in items_constellation:
        items_constellation[i['constellation']]+=1
    else:
        items_constellation[i['constellation']]=1
print(items_constellation)
max_radius_item = list()
for k in files_json:
    if k['radius'] > 396389911:
        max_radius_item.append(k)
with open(r'result_3_3_filter.json', 'w', encoding='utf-8') as file_filter:
    file_filter.write(json.dumps(max_radius_item, ensure_ascii=False))

df = pd.read_json('result_3_3.json')
item_age = df['radius'].describe()
print(item_age)
