# Исследовать структуру html-файлов, чтобы произвести парсинг всех данных.
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
import json
import pandas as pd
urls = list()
#собрали список ссылок
for i in range(1,1000):
    i = '3_var_7/'+str(i)+'.html'
    urls.append(i)
full_aside = list()
#записываем словарь значений. Если значение не найдено ставим пустуюс строку
for url in urls:
    with open(url, 'r', encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
        dom = etree.HTML(str(soup))
        item = {
            'Тип': ''.join(dom.xpath('substring-after(//*[contains(text(),"Тип")],":")')).strip(),
            'Турнир': ''.join(dom.xpath('substring-after(//h1[contains(text(),"Турнир")],":")')).strip(),
            'Адрес': {
                  'Город': ''.join(dom.xpath('substring-after(substring-before(//*[contains(text(),"Город")],"Начало"),"Город: ")')).strip(),
                   'Начало': ''.join(dom.xpath('substring-after(//*[contains(text(),"Начало:")],"Начало: ")')).strip(),
                },
            'Количество туров': ''.join(dom.xpath('substring-after(//*[contains(text(),"Количество туров")],":")')).strip(),
            'Контроль времени:': ''.join(dom.xpath('substring-after(//*[contains(text(),"Контроль времени:")],":")')).strip(),
            'Минимальный рейтинг для участия': ''.join(dom.xpath('substring-after(//*[contains(text(),"Минимальный рейтинг")],":")')).strip(),
            'Рейтинг': ''.join(dom.xpath('substring-after(//*[contains(text(),"Рейтинг")],":")')).strip(),
            'Изображение': ''.join(dom.xpath('//img/@src')),
            'Просмотры': ''.join(dom.xpath('substring-after(//*[contains(text(),"Просмотры")],":")')).strip(),
        }
        full_aside.append(item)
# записываем чистый json
with open(r'result_3_1.json', 'w', encoding='utf-8') as rezults:
    rezults.write(json.dumps(full_aside, ensure_ascii=False))
# открываем записанный json и делаем в нем сортироваку по рейтингу
with open('result_3_1.json', 'r', encoding='utf-8') as file:
    files = json.load(file)
    files_sort = sorted(files, key=lambda x: x['Рейтинг'], reverse=True)
# записываем отсортированный файл
with open(f'result_3_1_sort_rating.json', 'w', encoding='utf-8') as file_sort:
    file_sort.write(json.dumps(files_sort , ensure_ascii=False))
item_type = dict()
files_Olympic = list()
# для одного текстового поля посчитайте частоту меток, частота встречаемости по типу
for item in files:
    if item['Тип'] in item_type:
        item_type[item['Тип']]+=1
    else:
        item_type[item['Тип']]=1
print(item_type)
# фильтрация по типу
for item in files:
    if item['Тип'] == 'Olympic':
        files_Olympic.append(item)
# записываем в файл отфильтрованный список
with open(f'result_3_1_olympic.json', 'w', encoding='utf-8') as file_filter:
    file_filter.write(json.dumps(files_Olympic , ensure_ascii=False))
# выстчитываем статисчтические характеристики для столбца "Просмотры"
df = pd.read_json('result_3_1.json')
df_views = df['Просмотры'].describe()
print(df_views)
