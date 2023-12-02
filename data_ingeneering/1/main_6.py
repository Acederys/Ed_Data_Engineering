# Найти публичный API, который возвращает JSON с некоторыми данными.
# Необходимо получить данные в формате JSON,
# преобразовать в html представление в зависимости от содержания.
import json
from bs4 import BeautifulSoup
str_json = ''
with open('anime.json', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        str_json+=line
data = json.loads(str_json)
data = data['data']


all_id = list()
item_list = list()
for i in data:
    all_id.append(i)
    item_attr = i['attributes']
    item_titles = item_attr['titles']
    all_link = i['links']
    item = {
        'title': item_titles['ja_jp'],
        'desc': item_attr['description'],
        'link': all_link['self'],
        'subtype': item_attr['subtype'],
        'status': item_attr['status']
    }
    item_list.append(item)

soup = BeautifulSoup("""<table>
                    <tr>
                        <td>title</td>
                        <td>desc</td>
                        <td>links</td>
                        <td>subtype</td>
                        <td>status</td>
                    </tr>
                     </table>""",'html.parser')

table = soup.contents[0]
for tick in item_list:
    tr = soup.new_tag('tr')
    for key, val in tick.items():
        new_tag = soup.new_tag('td')
        tr.append(new_tag)
        new_tag.string = val
        td = soup.new_tag('td')
        td.string = val
    tr.append(new_tag)
    table.append(tr)
print(table)
with open(r'rezult_6.html','w', encoding='utf-8') as result:
        result.write(table.prettify())





