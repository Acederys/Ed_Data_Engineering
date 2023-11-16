# Исследовать структуру html-файлов, чтобы произвести парсинг всех данных.
# В каждом файле содержится информация об одном или нескольких объектах из случайной предметной области.
# Перечень всех характеристик объекта может меняться (у отдельного объекта могут отсутствовать некоторые характеристики).
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
import json
import pandas as pd
urls = list()
for i in range(1, 50):
    urls.append(f'3_2_var_7/{i}.html')
items = list()
for url in urls:
    with open(url, 'r', encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
        products = soup.find_all('div', class_="product-item")
        for product in products:
            dom = etree.HTML(str(product))
            item = {
                'data_id': ''.join(dom.xpath('//a[@class="add-to-favorite"]//@data-id')).strip(),
                'link': ''.join(dom.xpath('//*[@class="product-item"]/a[2]/@href')).strip(),
                'image': ''.join(dom.xpath('//*[@class="product-item"]/div[1]/img/@src')).strip(),
                'caption': ''.join(dom.xpath('//*[@class="product-item"]/span[1]/text()')).strip(),
                'price': int(dom.xpath('//*[@class="product-item"]/price/text()')[0].replace('₽','').replace(' ','')),
                'bonus': ''.join(dom.xpath('//*[@class="product-item"]/strong/text()')).strip(),
                'processor': ''.join(dom.xpath('//*[@class="product-item"]/ul/li[@type="processor"]/text()')).strip(),
                'ram': ''.join(dom.xpath('//*[@class="product-item"]/ul/li[@type="ram"]/text()')).strip(),
                'sim': ''.join(dom.xpath('//*[@class="product-item"]/ul/li[@type="sim"]/text()')).strip(),
                'matrix': ''.join(dom.xpath('//*[@class="product-item"]/ul/li[@type="matrix"]/text()')).strip(),
                'resolution': ''.join(dom.xpath('//*[@class="product-item"]/ul/li[@type="resolution"]/text()')).strip(),
                'camera': ''.join(dom.xpath('//*[@class="product-item"]/ul/li[@type="camera"]/text()')).strip(),
                'acc': ''.join(dom.xpath('//*[@class="product-item"]/ul/li[@type="acc"]/text()')).strip()
            }
            items.append(item)
# print(items)
with open(r'result_3_2.json', 'w', encoding='utf-8') as rezults:
    rezults.write(json.dumps(items, ensure_ascii=False))
with open('result_3_2.json', 'r', encoding='utf-8') as file:
    files = json.load(file)
    files_sort = sorted(files, key=lambda x: x['data_id'], reverse=True)
with open(r'result_3_2_sort.json', 'w', encoding='utf-8') as rezults_sort:
    rezults_sort.write(json.dumps(files_sort, ensure_ascii=False))
items_caption = dict()
for i in files_sort:
    if i['processor'] != '':
        if i['processor'] in items_caption:
            items_caption[i['processor']]+=1
        else:
            items_caption[i['processor']]=1
print(items_caption)
item_camera = list()
for item in files_sort:
    if item['camera'] != '':
        item_camera.append(item)
with open(r'result_3_2_filter.json', 'w', encoding='utf-8') as rezults_filter:
    rezults_filter.write(json.dumps(item_camera, ensure_ascii=False))

df = pd.read_json('result_3_2.json')
df_price = df['price'].describe()
print(df_price)

