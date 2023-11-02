# Считайте массив объектов в формате json.
# Агрегируйте информацию по каждому товару,
# получив следующую информацию: средняя цена, максимальная цена, минимальная цена.
# Сохранить полученную информацию по каждому объекту в формате json, а также в формате msgpack.
# Сравните размеры полученных файлов.

import json
import msgpack
import os
with open('products_7.json') as file:
    data = json.load(file)


    product_dict = {}
    for item in data:
        if item['name'] in product_dict:
            product_dict[item['name']].append(item['price'])
        else:
            product_dict[item['name']] = list()
            product_dict[item['name']].append(item['price'])
    result = list()
    for name, prices in product_dict.items():
        sum_elem = 0
        min_elem = prices[0]
        max_elem = prices[0]
        size = len(prices)
        for elem in prices:
            sum_elem +=elem
            min_elem = min(min_elem, elem)
            max_elem = max(max_elem, elem)
        result.append({
            'name': name,
            'sum': sum_elem,
            'min': min_elem,
            'max': max_elem,
            'avr': sum_elem/size
        })

    with open(r'result_2_3.json', 'w') as file_result:
        file_result.write(json.dumps(result))

    with open(r'result_2_3.msgpack', 'wb') as file_msgpack:
        file_msgpack.write(msgpack.dumps(result))

print(f'result : {os.path.getsize("result_2_3.json")}')
print(f'result : {os.path.getsize("result_2_3.msgpack")}')

