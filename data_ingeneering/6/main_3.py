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
start_colums = ['CANCELLED', 'AIRLINE',
                'TAIL_NUMBER', 'LATE_AIRCRAFT_DELAY',
                'TAXI_IN','ORIGIN_AIRPORT',
                'DEPARTURE_TIME', 'SCHEDULED_DEPARTURE',
                'FLIGHT_NUMBER','DAY_OF_WEEK']
#оптимизация датасета
# new_data_set = read_dataset(f'data/[3]flights.csv', f'result_6_3_statistic.json', f'result_6_3_statistic_clear.json', start_colums, f'dtypes_6_3.json', f'new_dataset_6_3.csv')

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


need_dtypes = read_types('dtypes_6_3.json')
dataset = pd.read_csv('new_dataset_6_3.csv',
                      usecols= lambda x: x in need_dtypes.keys(),
                      dtype=need_dtypes)
dataset.info(memory_usage='deep')

#
#Используя оптимизированный набор данных,
# построить пять-семь графиков
# (включая разные типы: линейный, столбчатый,
# круговая диаграмма, корреляция и т.д.)
# столбчатый
def hist_LATE_AIRCRAFT_DELAY():
    plt.figure(figsize=(30, 5))
    plt.title('LATE_AIRCRAFT_DELAY', fontsize=18)
    sort_dow = dataset['LATE_AIRCRAFT_DELAY'].sort_index()
    plot = sort_dow.hist()
    plot.get_figure().savefig('6_3_hist_LATE_AIRCRAFT_DELAY.png')

# столбчатый
def hist_AIRLINE():
    plt.figure(figsize=(30, 5))
    plt.title('AIRLINE', fontsize=18)
    sort_dow = dataset['AIRLINE'].sort_index()
    plot = sort_dow.hist()
    plot.get_figure().savefig('6_3_hist_AIRLINE.png')

# линейный
def plot_DEPARTURE_TIME():
    plt.figure(figsize=(30, 5))
    plt.title('DEPARTURE_TIME', fontsize=18)
    sort_dow = dataset['DEPARTURE_TIME'].sort_index()
    plot = sort_dow.plot()
    plot.get_figure().savefig('6_3_DEPARTURE_TIME.png')

# линейный
def plot_TAXI_IN():
    plt.figure(figsize=(30, 5))
    plt.title('TAXI_IN', fontsize=18)
    sort_dow = dataset['TAXI_IN'].sort_index()
    plot = sort_dow.plot()
    plot.get_figure().savefig('6_3_plot_TAXI_IN.png')

# круговая диаграмма
def show_DAY_OF_WEEK():
    plt.figure(figsize=(10, 10))
    plt.title('DAY_OF_WEEK', fontsize=18)
    plot_data = dataset['DAY_OF_WEEK'].value_counts()
    plot_data.name = ''
    plot = plot_data.plot(kind='pie', fontsize=18, autopct='%1.0f%%')
    plot.get_figure().savefig('6_3_show.png')


# корреляция
# def corr():
#     data = dataset.copy()
#     data.vf_ModelYear = data.vf_ModelYear.astype(int)
#     data = data.select_dtypes(include=[int, float])
#     plot = plt.figure(figsize=(16,16))
#     sns.heatmap(data.corr())
#     plot.get_figure().savefig('6_2_corr.png')
hist_LATE_AIRCRAFT_DELAY()
hist_AIRLINE()
plot_DEPARTURE_TIME()
plot_TAXI_IN()
show_DAY_OF_WEEK()
