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
start_colums = ['year', 'timbre_avg_0',
                'timbre_avg_1', 'timbre_avg_2',
                'timbre_avg_3','timbre_avg_4',
                'timbre_avg_5', 'timbre_avg_6',
                'timbre_avg_7','timbre_avg_8']
#оптимизация датасета
# new_data_set = read_dataset(f'data/songs.csv', f'result_6_6_statistic.json', f'result_6_6_statistic_clear.json', start_colums, f'dtypes_6_6.json', f'new_dataset_6_6.csv')

# чтение чистого датаесета
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


need_dtypes = read_types('dtypes_6_6.json')
dataset = pd.read_csv('new_dataset_6_6.csv',
                      usecols= lambda x: x in need_dtypes.keys(),
                      dtype=need_dtypes)
dataset.info(memory_usage='deep')

#
#Используя оптимизированный набор данных,
# построить пять-семь графиков
# (включая разные типы: линейный, столбчатый,
# круговая диаграмма, корреляция и т.д.)
# столбчатый
def hist_timbre_avg_0():
    plt.figure(figsize=(30, 5))
    plt.title('timbre_avg_0', fontsize=18)
    sort_dow = dataset['timbre_avg_0'].sort_index()
    plot = sort_dow.hist()
    plot.get_figure().savefig('6_6_hist_timbre_avg_0.png')

# столбчатый
def hist_timbre_avg_1():
    plt.figure(figsize=(30, 5))
    plt.title('timbre_avg_1', fontsize=18)
    sort_dow = dataset['timbre_avg_1'].sort_index()
    plot = sort_dow.hist()
    plot.get_figure().savefig('6_6_hist_timbre_avg_1.png')

# линейный
def plot_timbre_avg_2():
    plt.figure(figsize=(30, 5))
    plt.title('timbre_avg_2', fontsize=18)
    sort_dow = dataset['timbre_avg_2'].sort_index()
    plot = sort_dow.plot()
    plot.get_figure().savefig('6_6_timbre_avg_2.png')

# линейный
def plot_timbre_avg_3():
    plt.figure(figsize=(30, 5))
    plt.title('timbre_avg_3', fontsize=18)
    sort_dow = dataset['timbre_avg_3'].sort_index()
    plot = sort_dow.plot()
    plot.get_figure().savefig('6_6_plot_timbre_avg_3.png')

# круговая диаграмма
def show_year():
    plt.figure(figsize=(10, 10))
    plt.title('year', fontsize=18)
    plot_data = dataset['year'].value_counts()
    plot_data.name = ''
    plot = plot_data.plot(kind='pie', fontsize=18, autopct='%1.0f%%')
    plot.get_figure().savefig('6_6_show.png')


# корреляция
# def corr():
#     data = dataset.copy()
#     data.vf_ModelYear = data.vf_ModelYear.astype(int)
#     data = data.select_dtypes(include=[int, float])
#     plot = plt.figure(figsize=(16,16))
#     sns.heatmap(data.corr())
#     plot.get_figure().savefig('6_6_corr.png')
hist_timbre_avg_0()
hist_timbre_avg_1()
plot_timbre_avg_2()
plot_timbre_avg_3()
show_year()
