# Считайте файл согласно вашему варианту. В строках имеются пропуски,
# обозначенные «NA» – замените их, рассчитав среднее значение соседних чисел.
# Затем отфильтруйте значения на каждой строке, исключив те числа, корень квадратный
# из которых будет меньше .
# В результирующем файле запишите полученные данные.
import math
with open('text_3_var_7') as file:
    lines = file.readlines()
new_list = list()
for line in lines:
    items = line.split(',')
    for elem in range(len(items)):
        if items[elem] == 'NA':
            items[elem] = (int(items[elem-1]) + int(items[elem+1])/2)
    filter_list = list()
    for i in items:
        float_num = float(i)
        if math.sqrt(float_num) > 57:
            filter_list.append(int(float_num))
    new_list.append(filter_list)
print(new_list)
with open(r'result_3.txt', 'w') as results:
    for row in new_list:
        for value in row:
            results.write(str(value) + ',')
        results.write('\n')
