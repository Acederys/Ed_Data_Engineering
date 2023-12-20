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
start_colums = ['color', 'brandName',
                'vf_ModelYear', 'isNew',
                'vf_Turbo','vf_ValveTrainDesign',
                'vf_TractionControl', 'vf_TrailerType',
                'askPrice','vf_Model']
#оптимизация датасета
#new_data_set = read_dataset(f'data/[2]automotive.csv.zip', f'result_6_2_statistic.json', f'result_6_2_statistic_clear.json', start_colums, f'dtypes_6_2.json', f'new_dataset_6_2.csv')

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


need_dtypes = read_types('dtypes_6_2.json')
dataset = pd.read_csv('new_dataset_6_2.csv',
                      usecols= lambda x: x in need_dtypes.keys(),
                      dtype=need_dtypes)
dataset.info(memory_usage='deep')

#
#Используя оптимизированный набор данных,
# построить пять-семь графиков
# (включая разные типы: линейный, столбчатый,
# круговая диаграмма, корреляция и т.д.)
# столбчатый
def hist_askPrice():
    plt.figure(figsize=(30, 5))
    plt.title('askPrice', fontsize=18)
    sort_dow = dataset['askPrice'].sort_index()
    plot = sort_dow.hist()
    plot.get_figure().savefig('6_2_hist_askPrice.png')

# столбчатый
def hist_brandName():
    plt.figure(figsize=(30, 5))
    plt.title('brandName', fontsize=18)
    sort_dow = dataset['brandName'].sort_index()
    plot = sort_dow.hist()
    plot.get_figure().savefig('6_2_hist_modelName.png')

# линейный
def plot_ModelYear():
    plt.figure(figsize=(30, 5))
    plt.title('vf_ModelYear', fontsize=18)
    sort_dow = dataset['vf_ModelYear'].sort_index()
    plot = sort_dow.plot()
    plot.get_figure().savefig('6_2_ModelYear.png')

# линейный
def plot_askPrice():
    plt.figure(figsize=(30, 5))
    plt.title('askPrice', fontsize=18)
    sort_dow = dataset['askPrice'].sort_index()
    plot = sort_dow.plot()
    plot.get_figure().savefig('6_2_plot_askPrice.png')

# круговая диаграмма
def show_Turbo():
    plt.figure(figsize=(10, 10))
    plt.title('vf_Turbo', fontsize=18)
    plot_data = dataset['vf_Turbo'].value_counts()
    plot_data.name = ''
    plot = plot_data.plot(kind='pie', fontsize=18, autopct='%1.0f%%')
    plot.get_figure().savefig('6_2_show.png')


# корреляция
# def corr():
#     data = dataset.copy()
#     data.vf_ModelYear = data.vf_ModelYear.astype(int)
#     data = data.select_dtypes(include=[int, float])
#     plot = plt.figure(figsize=(16,16))
#     sns.heatmap(data.corr())
#     plot.get_figure().savefig('6_2_corr.png')
hist_askPrice()
hist_brandName()
plot_ModelYear()
plot_askPrice()
show_Turbo()
