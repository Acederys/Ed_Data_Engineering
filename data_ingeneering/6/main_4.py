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
start_colums = ['type_name', 'employment_name',
                'response_url', 'accept_kids',
                'area_id','apply_alternate_url',
                'address_lng', 'address_street',
                'address_lat','archived']
#оптимизация датасета
# new_data_set = read_dataset(f'data/[4]vacancies.csv.gz', f'result_6_4_statistic.json', f'result_6_4_statistic_clear.json', start_colums, f'dtypes_6_4.json', f'new_dataset_6_4.csv')

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


need_dtypes = read_types('dtypes_6_4.json')
dataset = pd.read_csv('new_dataset_6_4.csv',
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
def hist_address_lng():
    plt.figure(figsize=(30, 5))
    plt.title('address_lng', fontsize=18)
    sort_dow = dataset['address_lng'].sort_index()
    plot = sort_dow.hist()
    plot.get_figure().savefig('6_4_hist_address_lng.png')

# столбчатый
def hist_employment_name():
    plt.figure(figsize=(30, 5))
    plt.title('employment_name', fontsize=18)
    sort_dow = dataset['employment_name'].sort_index()
    plot = sort_dow.hist()
    plot.get_figure().savefig('6_4_hist_employment_name.png')

# линейный
def plot_area_id():
    plt.figure(figsize=(30, 5))
    plt.title('area_id', fontsize=18)
    sort_dow = dataset['area_id'].sort_index()
    plot = sort_dow.plot()
    plot.get_figure().savefig('6_4_area_id.png')

# линейный
def plot_address_lat():
    plt.figure(figsize=(30, 5))
    plt.title('address_lat', fontsize=18)
    sort_dow = dataset['address_lat'].sort_index()
    plot = sort_dow.plot()
    plot.get_figure().savefig('6_4_plot_address_lat.png')

# круговая диаграмма
def show_archived():
    plt.figure(figsize=(10, 10))
    plt.title('archived', fontsize=18)
    plot_data = dataset['archived'].value_counts()
    plot_data.name = ''
    plot = plot_data.plot(kind='pie', fontsize=18, autopct='%1.0f%%')
    plot.get_figure().savefig('6_4_show.png')


# корреляция
# def corr():
#     data = dataset.copy()
#     data.vf_ModelYear = data.vf_ModelYear.astype(int)
#     data = data.select_dtypes(include=[int, float])
#     plot = plt.figure(figsize=(16,16))
#     sns.heatmap(data.corr())
#     plot.get_figure().savefig('6_2_corr.png')
hist_address_lng()
hist_employment_name()
plot_area_id()
plot_address_lat()
show_archived()
