import pandas as pd
import matplotlib
import numpy as np
import json
import os
import zipfile
from memory_calc import memory_cal
from write_to_json import write_to_json
from col_category import col_category, mem_usage
from col_num import col_num_int, col_num_float
def read_dataset(file_name, statistic_json, statistic_clear_json, colums_names, type_format, new_dataset):
    # Загрузить набор данных из файла
    pd.set_option("display.max_rows", 20, "display.max_columns", 60)
    # file_name = 'data/[1]game_logs.csv'
    # dataset = pd.read_csv(file_name)
    dataset = pd.read_csv(file_name, compression='zip')
    column_stat = memory_cal(file_name, dataset)
    # запись в json
    write_to_json(column_stat, statistic_json)

    # Преобразовать все колонки с типом данных «object» в категориальные,
    # если количество уникальных значений колонки составляет менее 50%.
    converted_odj = col_category(dataset)

    # Провести понижающее преобразование типов «int» колонок

    converted_int = col_num_int(dataset)
    # Провести понижающее преобразование типов «float» колонок
    converted_float = col_num_float(dataset)
    # Повторно провести анализ набора данных, как в п. 2,
    # сравнив показатели занимаемой памяти

    optimized_dataset = dataset.copy()
    optimized_dataset[converted_odj.columns] = converted_odj
    optimized_dataset[converted_int.columns] = converted_int
    optimized_dataset[converted_float.columns] = converted_float

    column_stat_clear = memory_cal(file_name, optimized_dataset)
    write_to_json(column_stat_clear, statistic_clear_json)

    # Выбрать произвольно 10 колонок для дальнейшем работы,
    # прописав преобразование типов и загрузку только нужных данных на этапе чтения файла.
    # При этом стоит использовать чанки.
    # Сохраните полученный поднабор в отдельном файле.

    opt_dtypes = optimized_dataset.dtypes
    need_colum = {}
    for key in colums_names:
        need_colum[key] = opt_dtypes[key]

    with open(type_format, mode="w") as file:
        dtype_json = need_colum.copy()
        for key in dtype_json.keys():
            dtype_json[key] = str(dtype_json[key])
        json.dump(dtype_json, file)

    has_header = True
    for chunk in pd.read_csv(file_name,
                             usecols = lambda x: x in colums_names,
                             dtype = need_colum,
                             # infer_datetime_format=True,
                             chunksize=100_000):
        print(mem_usage(chunk))
        chunk.to_csv(new_dataset, mode="a", header=has_header)
        has_header = False
