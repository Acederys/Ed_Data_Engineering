# # Считайте массив объектов в формате json.
# # Агрегируйте информацию по каждому товару,
# # получив следующую информацию: средняя цена, максимальная цена, минимальная цена.
# # Сохранить полученную информацию по каждому объекту в формате json, а также в формате msgpack.
# # Сравните размеры полученных файлов.
# import json
# str_json = ''
# with open('products_7.json', encoding='utf-8') as data:
#     lines = data.readlines()
#     for elem in lines:
#         str_json+=elem
#
# data = json.loads(str_json)
# print(data[0])
# name = []
# list_prod = []
# dict_product ={}
# # dict_product = dict()
# # list_prod = list()
# # список всех названий
# for i in data:
#     list_prod.append(i['name'])
# # # словарь названий и сколько раз их продали
# for i in list_prod:
#     # print(i)
#     if i in dict_product:
#         dict_product[i]+=1
#     else:
#         dict_product[i]=1
#
# for k in dict_product.items():
#     print(k[0])
#
# for i in range(0,len(data)):
#     elem = data[i]
#     # if elem['name'] is not name:
#     #     name.append(elem['name'])
#     #     print(name)
#     # print(elem['name'], elem['price'])
# # for i in data:
# #     print(i['name'])
# # count = 0
# # for j in dict_product.items():
# #     for i in data:
# #         if i['name'] == j[0]:
# #             count = count + i['price']
# #             print(j[0],j[1])
# #             print(i['name'], count)
# #         print(i['name'], count)
#
#
#     # if elem['name'] is dict_product:
#     #     dict_product['name'] = elem['name']
#     #     dict_product['price'] = elem['price']
#     #     print(dict_product['name'])
#     #     print(dict_product['price'])
#
