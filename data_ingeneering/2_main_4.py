# Считайте данные в формате pkl о товарах.
# Также считайте данные из файла формата json о новых ценах для каждого товара:
#
# {
#
#     name: "Apple",
#
#     method: "add"|"sub"|"percent+"|"percent-",
#
#     param: 4|0.01
#
# }
#
# Обновите цены для товаров в зависимости от метода:
#
# "add" – добавить значение param к цене;
#
# "sub" – отнять значение param от цены;
#
# "percent+" – поднять на param % (1% = 0.01);
#
# "percent-" – снизить на param %.
#
# Сохраните модифицированные данные обратно в формат pkl.
import json
import pickle

# функция для высчитывая обнолвения цены
def  update_priece(price, param):
    method = param["method"]
    if method == 'add':
        price['price'] += param['param']
    elif method == 'sub':
        price['price'] -= param['param']
    elif method == 'percent+':
        price['price'] += (price['price'] * param['param'])
    elif method == 'percent-':
        price['price'] -= (price['price'] * param['param'])
    price['price'] = round(price["price"], 2)


with open('products_7.pkl', 'rb') as file:
    data = pickle.load(file)

with open('price_info_7.json') as file_json:
    data_json = json.load(file_json)

products = dict()

for elem in data_json:
    products[elem['name']] = elem

# Ищем элемент файле с ценами
for elem in data:
    # соединяем имена из двух словарей
    item = products[elem['name']]
    update_priece(elem, item)

with open(r'result_2_4.pkl', 'wb') as result:
    result.write(pickle.dumps(data))



