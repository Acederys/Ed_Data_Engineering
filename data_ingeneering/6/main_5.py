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
start_colums = ['diameter', 'orbit_id',
                'name', 'class',
                'sigma_q','moid_ld',
                'neo', 'albedo',
                'epoch','equinox']
#оптимизация датасета
# new_data_set = read_dataset(f'data/[5]asteroid.zip', f'result_6_5_statistic.json', f'result_6_5_statistic_clear.json', start_colums, f'dtypes_6_5.json', f'new_dataset_6_5.csv')

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


need_dtypes = read_types('dtypes_6_5.json')
dataset = pd.read_csv('new_dataset_6_5.csv',
                      usecols= lambda x: x in need_dtypes.keys(),
                      dtype=need_dtypes)
dataset.info(memory_usage='deep')
#
# #
#Используя оптимизированный набор данных,
# построить пять-семь графиков
# (включая разные типы: линейный, столбчатый,
# круговая диаграмма, корреляция и т.д.)
# столбчатый
def hist_albedo():
    plt.figure(figsize=(30, 5))
    plt.title('albedo', fontsize=18)
    sort_dow = dataset['albedo'].sort_index()
    plot = sort_dow.hist()
    plot.get_figure().savefig('6_5_hist_albedo.png')

# столбчатый
def hist_neo():
    plt.figure(figsize=(30, 5))
    plt.title('neo', fontsize=18)
    sort_dow = dataset['neo'].sort_index()
    plot = sort_dow.hist()
    plot.get_figure().savefig('6_5_hist_neo.png')

# линейный
def plot_diameter():
    plt.figure(figsize=(30, 5))
    plt.title('diameter', fontsize=18)
    sort_dow = dataset['diameter'].sort_index()
    plot = sort_dow.plot()
    plot.get_figure().savefig('6_5_diameter.png')

# линейный
def plot_epoch():
    plt.figure(figsize=(30, 5))
    plt.title('epoch', fontsize=18)
    sort_dow = dataset['epoch'].sort_index()
    plot = sort_dow.plot()
    plot.get_figure().savefig('6_5_plot_epoch.png')

# круговая диаграмма
def show_class():
    plt.figure(figsize=(10, 10))
    plt.title('class', fontsize=18)
    plot_data = dataset['class'].value_counts()
    plot_data.name = ''
    plot = plot_data.plot(kind='pie', fontsize=18, autopct='%1.0f%%')
    plot.get_figure().savefig('6_5_show.png')


# корреляция
# def corr():
#     data = dataset.copy()
#     data.vf_ModelYear = data.vf_ModelYear.astype(int)
#     data = data.select_dtypes(include=[int, float])
#     plot = plt.figure(figsize=(16,16))
#     sns.heatmap(data.corr())
#     plot.get_figure().savefig('6_2_corr.png')
hist_albedo()
hist_neo()
plot_diameter()
plot_epoch()
show_class()
