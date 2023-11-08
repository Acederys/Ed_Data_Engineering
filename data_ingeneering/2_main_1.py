# Загрузите матрицу из файла с форматом npy.
# Подсчитайте сумму всех элементов и их среднее арифметическое, подсчитайте сумму
# и среднее арифметическое главной и побочной диагоналей матрицы. Найдите
# максимальное и минимальное значение. Полученные значения запишите в json следующего формата:
# {
#     sum: 4,
#     avr: 4,
#     sumMD: 4, // главная диагональ
#     avrMD: 5,
#     sumSD: 4, // побочная диагональ
#     avrSD: 5,
#     max: 4,
#     min: 2
# }
# Исходную матрицу необходимо нормализовать и сохранить в формате npy.
import json
import numpy as np
data = np.load('matrix_1_7.npy')
# print(data)
data_len = len(data)
sum_elem = 0
avr_elem = 0
sumMD_elem = 0
avrMD_elem = 0
sumSD_elem = 0
avrSD_elem = 0
max_elem = data[0][0]
min_elem = data[0][0]
item = dict()
# перебор всех элементов матрицы. Идем от 0 до 22 строки, потом с 0 до 22 элемента внутри строки
for i in range(0,data_len):
    for j in range(0,data_len):
        sum_elem+=data[i][j]
        if i == j:
            sumMD_elem+= data[i][j]
        elif i+j == (data_len-1):
            sumSD_elem += data[i][j]
        max_elem = max(max_elem, data[i][j])
        min_elem = min(min_elem, data[i][j])

item = {
    'sum': float(sum_elem),
    'avr': float(sum_elem/(data_len*data_len)),
    'sumMD': float(sumMD_elem),
    'avrMD': float(sumMD_elem/data_len),
    'sumSD': float(sumSD_elem),
    'avrSD': float(sumSD_elem/data_len),
}

with open('result_2_1.json', 'w') as results:
    results.write(json.dumps(item))

new_matrix = list()
for string in data:
    string_new = []
    for elem in string:
        elem = elem/sum_elem
        string_new.append(elem)
    new_matrix.append(string_new)

matrix = np.array(new_matrix, dtype=float)
print(matrix)
np.save(r'normalize', matrix)



