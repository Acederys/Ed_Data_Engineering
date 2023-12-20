import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import seaborn as sns
import os
from memory_calc import memory_cal
from write_to_json import write_to_json
from col_category import col_category, mem_usage
from col_num import col_num_int, col_num_float
from main_optimizired import read_dataset

pd.set_option("display.max_rows", 20, "display.max_columns", 60)
# выбранные столбцы
start_colums = ['date', 'number_of_game',
                'day_of_week', 'v_manager_name',
                'park_id','length_minutes',
                'h_walks', 'h_hits',
                'v_hits','h_errors']
#оптимизация датасета
# new_data_set = read_dataset(f'data/[1]game_logs.csv', f'result_6_1_statistic.json', f'result_6_1_statistic_clear.json', start_colums, f'dtypes_6_1.json', f'new_dataset_6_1.csv')


#чтение чистого датаесета
def read_file(file_name):
    return pd.read_csv(file_name)


def read_types(file_name):
    dtypes= {}
    with open(file_name, mode='r') as file:
        dtypes = json.load(file)

    for key in dtypes.keys():
        if dtypes[key] == 'category':
            dtypes[key] = pd.CategoricalDtype
        else:
            dtypes[key] = np.dtype(dtypes[key])
    return dtypes


need_dtypes = read_types('dtypes_6_1.json')
dataset = pd.read_csv('new_dataset_6_1.csv',
                      usecols= lambda x: x in need_dtypes.keys(),
                      dtype=need_dtypes)
dataset.info(memory_usage='deep')


#Используя оптимизированный набор данных,
# построить пять-семь графиков
# (включая разные типы: линейный, столбчатый,
# круговая диаграмма, корреляция и т.д.)
# столбчатый
plt.figure(figsize=(30, 5))
sort_dow = dataset['day_of_week'].sort_index()
plot = sort_dow.hist()
plot.get_figure().savefig('6_1_hist.png')

# столбчатый
plt.figure(figsize=(30, 5))
sort_dow = dataset['park_id'].sort_index()
plot = sort_dow.hist()
plot.get_figure().savefig('6_1_hist_park_id.png')

# линейный
plt.figure(figsize=(30, 5))
sort_dow = dataset['h_hits'].sort_index()
plot = sort_dow.plot()
plot.get_figure().savefig('6_1_plot.png')

# линейный
plt.figure(figsize=(30, 5))
sort_dow = dataset['h_errors'].sort_index()
plot = sort_dow.plot()
plot.get_figure().savefig('6_1_plot_errors.png')

# круговая диаграмма
# fig1, ax1 = plt.subplots()
# plot = ax1.pie(dataset['h_errors'], dataset['day_of_week'])
# plot.get_figure().savefig('6_1_show.png')


# корреляция
data = dataset.copy()
data.date = data.date.astype(int)
data = data.select_dtypes(include=[int, float])
plt.figure(figsize=(16,16))
sns.heatmap(data.corr())
plot.get_figure().savefig('6_1_corr.png')
