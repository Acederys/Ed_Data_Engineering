# Задание 2

# Считайте файл согласно вашему варианту и подсчитайте среднее арифметическое чисел по
# каждой строке. В результирующем файле выведите полученные данные:
#
# average1
#
# average2
#
# average3
#
# -----------
#
# averageN

# data_num = open('text_2_var_7').read()

with open('text_2_var_7')as file:
    lines = file.readlines()
sum_lines = list()

for line in lines:
        nums = line.split(" ")
        avage = 0
        sum_line = 0
        for num in nums:
            sum_line += int(num)
            avage = sum_line//len(nums)
        sum_lines.append(avage)
print(sum_lines)

with open(r'result_2.txt', 'w') as result:
    for value in sum_lines:
        result.write(str(value) + '\n')
