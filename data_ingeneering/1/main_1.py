# Считайте файл согласно вашему варианту и подсчитайте частоту каждого слова в тексте.
# В результирующем файле выведите полученные данные в порядке убывания:

with open('text_1_var_7') as file:
    data = file.read()
data = sorted(data.replace('.', ' ').replace(',', ' ').replace('!', ' ').replace('?', ' ').split())
dict_numb = dict()
for item in data:
    if item in dict_numb:
        dict_numb[item]+=1
    else:
        dict_numb[item]=1
results = (dict(sorted(dict_numb.items(), reverse=True, key= lambda item: item[1])))
with open(r'result_1.txt', 'w', encoding='utf-8') as result:
    for key, value in results.items():
        result.write(key + ':' + str(value) + '\n')
