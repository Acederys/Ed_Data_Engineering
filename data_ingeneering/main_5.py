# Считайте фрагмент html из файла согласно варианту.
# Извлеките данные из таблицы html.
# Запишите полученный csv файл.

from bs4 import BeautifulSoup
import csv
new_list = list()
with open('text_5_var_7', encoding='utf-8') as file:
    data = file.readlines()
    html = ''
    for line in data:
        html +=line

    soup = BeautifulSoup(html, 'html.parser')
    all_content = soup.find_all('tr')
    all_content = all_content[1:]
    for j in all_content:
        row = j.find_all('td')
        item = {
            'Company': row[0].text,
            'Contact': row[1].text,
            'Country': row[2].text,
            'Price': row[3].text,
            'Item': row[4].text,
        }
        new_list.append(item)

with open(r'result_5.csv','w', encoding='utf-8', newline='') as results:
    writer = csv.writer(results, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for item in new_list:
        writer.writerow(item.values())

