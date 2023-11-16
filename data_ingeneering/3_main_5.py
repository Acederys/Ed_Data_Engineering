# Самостоятельно найти сайт, соответствующий следующим условиям:
#
# непопулярный, регионального уровня или из узкой области (с целью избежать дублирования)
#
# наличие страниц-каталогов, где есть информация сразу по нескольких объектам
#
# наличие страниц, посвященных отдельному объекту
#
#  Необходимо:
#
# спарсить нескольких страниц (минимум 10), посвященных только одному объекту;
#
# спарсить страницы-каталоги, где размещена информация сразу по нескольким объектам.
#
# Данные можно скачать и сохранить локально в виде html, а можно организовать их получение напрямую через обращение к серверу сайта.
#
# Результаты парсинга собрать отдельно по каждой подзадаче и записать в отдельный json.
#
# Выполните произвольные операции с данными:
#
# отсортируйте значения по одному из доступных полей
#
# выполните фильтрацию по другому полю (запишите результат отдельно)
#
# для одного выбранного числового поля посчитайте показатели статистики
#
# для одного текстового поля посчитайте частоту меток.
from bs4 import BeautifulSoup
import json
import pandas as pd
from lxml import etree
import requests
#спарсили страницы каталога с сайта
r = requests.get('https://www.ats-com.ru/catalog/ericsson-lg', auth=('user', 'pass'))
soup = BeautifulSoup(r.content, 'html.parser')
dom = etree.HTML(str(soup))
all_links = dom.xpath('//*[@class="catalog-main-prod"]//li/a/@href')
urls = []
for i in all_links:
    urls.append(f'https://www.ats-com.ru/{i}')

items = []
for elem in urls:
    url = requests.get(elem)
    soup = BeautifulSoup(url.content, 'html.parser')
#записали страницы каталога в файл
for i in range(0,len(items)):
    with open(f'3_5_html/{i}.html','w', encoding='utf-8') as result_file:
            result_file.write(items[i].prettify())
links = list()
links_item = []
# записали все ссылки на каталоги
for i in range(0,6):
    links.append(f'3_5_html/{i}.html')
product_list =list()
# записали все данные с каталога
for link in links:
    with open(link, 'r', encoding='utf-8') as data:
        soup = BeautifulSoup(data, 'html.parser')
        products = soup.find_all('li', class_="product")
        for product in products:
            dom = etree.HTML(str(product))
            links_item.append(''.join(dom.xpath('//h3/a/@href')).strip())
            item = {
                'caption': ''.join(dom.xpath('//h3//text()')).strip(),
                'price': float(''.join(dom.xpath('//*[@class="price"]/text()')).replace(' ','').replace(',','.').strip()),
                'compare_price': ''.join(dom.xpath('//*[@class="compare_price"]/text()')).replace(' ','').replace(',','.').strip(),
            }
            product_list.append(item)
full_item = []
# забираем все страницы продуктов
for links_item in links_item:
    r_item = requests.get(f'https://www.ats-com.ru/{links_item}', auth=('user', 'pass'))
    soup_item = BeautifulSoup(r_item.content, 'html.parser')
    full_item.append(soup_item)
# print(full_item)
# записываем все страницы продуктов
for i in range(1,len(full_item)):
    with open(f'3_5_html/poduct_{i}.html','w', encoding='utf-8') as result:
            result.write(full_item[i].prettify())
# записываем рузультирующий json для каталогов
with open(r'result_3_5.json', 'w', encoding='utf-8') as rezults:
    rezults.write(json.dumps(product_list, ensure_ascii=False))
all_element = list()
# собираем данные со станиц продуктов
for i in range(1, 83):
    with open(f'3_5_html/poduct_{i}.html','r', encoding='utf-8') as file_products:
        soup = BeautifulSoup(file_products, 'html.parser')
        proct_item = soup.find_all('div', class_="row product")
        dom_product = etree.HTML(str(proct_item))
        element = {
            'caption': ''.join(dom_product.xpath('//h1/text()')).strip(),
            'description': ''.join(dom_product.xpath('//*[@class="description"]//text()')).replace('\n','').strip(),
            'price': float(''.join(dom_product.xpath('//*[@class="price"]/text()')).replace(' ','').replace(',','.').strip()),
            'compare_price': ''.join(dom_product.xpath('//*[@class="compare_price"]/text()')).replace(' ','').replace(',','.').strip(),
            }
        all_element.append(element)
# записываем json для продуктов
with open(r'result_3_5_elem.json', 'w', encoding='utf-8') as elem_pr:
    elem_pr.write(json.dumps(all_element, ensure_ascii=False))

with open('result_3_5.json', 'r', encoding='utf-8') as file:
    files = json.load(file)
    files_sort = sorted(files, key=lambda x: x['price'], reverse=True)
with open(r'result_3_5_sort.json', 'w', encoding='utf-8') as rezults_sort:
    rezults_sort.write(json.dumps(files_sort, ensure_ascii=False))
items_caption = dict()
for i in files_sort:
    if i['price'] != '':
        if i['price'] in items_caption:
            items_caption[i['price']]+=1
        else:
            items_caption[i['price']]=1
print(items_caption)
item_compare_price = list()
for item in files_sort:
    if item['compare_price'] != '':
        item_compare_price.append(item)
with open(r'result_3_5_filter.json', 'w', encoding='utf-8') as rezults_filter:
    rezults_filter.write(json.dumps(item_compare_price, ensure_ascii=False))

df = pd.read_json('result_3_5.json')
df_price = df['price'].describe()
print(df_price)


