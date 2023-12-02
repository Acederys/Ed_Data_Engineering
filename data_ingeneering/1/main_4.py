# Считайте csv файл согласно вашему варианту. Структура файла имеет
# следующий вид по колонкам в порядке их следования: порядковый номер, имя,
# фамилия, возраст, доход, номер телефона.
#
# Необходимо выполнить следующие действия:
#
# Удалить колонку с номером телефона
#
# Рассчитайте средний доход по данным, а затем отфильтруйте те строки, доход
# которых меньше среднего.
#
# Также примените фильтр по колонке возраст, оставив строки со значением более
#
# Запишите полученные результаты в новый файл csv, произведя при этом сортировку
# по полю номер (по возрастанию):

#заголовок для примера

#id,name,age,salary

# 1, Connor John, 25, 1000₽
import csv
i = 0
new_list = list()
with open('text_4_var_7', newline='\n', encoding='utf-8') as file:
    data = csv.reader(file, delimiter=',')
    # убираем колонку с номером телеона
    for row in data:
        item = {
            'number': int(row[0]),
            'name': row[2] + ' ' + row[1],
            'age': int(row[3]),
            'salary': int(row[4].replace("₽",""))
        }
        # сумма всего дохода
        i +=item['salary']
        new_list.append(item)
    avage = i/len(new_list)
    # print(avage)
    filter_list = list()
    option_for_age = 25+(7%10)
    for row in new_list:
        if row['salary'] >= avage and row['age']>option_for_age:
            filter_list.append(row)
result_list = sorted(filter_list, key=lambda i:i['number'])

with open(r'result_4.csv', 'w',encoding='utf-8', newline='') as results:
    writer = csv.writer(results, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    for item in result_list:
        writer.writerow(item.values())


