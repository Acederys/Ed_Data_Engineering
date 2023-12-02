# Загрузите матрицу из файла с форматом npy.
# Создайте три массива x, y, z . Отберите из матрицы значения,
# которые превышают следующее значение: 500+ вариант, следующим образом:
# индексы элемента разнесите по массивам x, y, а само значение в массив z.
# Сохраните полученные массив в файла формата npz.
# Воспользуйтесь методами np.savez() и np.savez_compressed().
# Сравните размеры полученных файлов.
import os.path

import numpy as np

data = np.load('matrix_7_2.npy')
x = list()
y = list()
z = list()
data_size = len(data)
# высчитываем индекс. 500+ номер варианта
element = 500+7
for i in range(0,data_size):
    for j in range(0,data_size):
        if data[i][j] > element:
            x.append(i)
            y.append(j)
            z.append(data[i][j])
np.savez(r'result_2_2',x=x, y=y, z=z)
np.savez_compressed(r'result_2_2_com', x=x, y=y, z=z)
print(f'result : {os.path.getsize("result_2_2.npz")}')
print(f'result_compressed : {os.path.getsize("result_2_2_com.npz")}')

