import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import seaborn as sns
import os
from sklearn.preprocessing import OrdinalEncoder
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

# преобразовываем категориальные признаки в числовые
def transform_category():
    cat_columns = [] # создаем пустой список для имен колонок категориальных данных
    num_columns = [] # создаем пустой список для имен колонок числовых данных
    for column_name in dataset.columns: # смотрим на все колонки в датафрейме
        if (dataset[column_name].dtypes == 'category'): # проверяем тип данных для каждой колонки
            cat_columns +=[column_name] # если тип объект - то складываем в категориальные данные
        else:
            num_columns +=[column_name] # иначе - числовые)
    ordinal = OrdinalEncoder()
    ordinal.fit(dataset[cat_columns])
    Ordinal_encoded = ordinal.transform(dataset[cat_columns])
    df_ordinal = pd.DataFrame(Ordinal_encoded, columns = cat_columns)
    df = pd.concat([dataset[num_columns], df_ordinal], axis=1)
    return df
df = transform_category()
#Используя оптимизированный набор данных,
# построить пять-семь графиков
# (включая разные типы: линейный, столбчатый,
# круговая диаграмма, корреляция и т.д.)
# столбчатый
# чтобы построить график надо удалить выбросы
def figure_1(dataset):
    x = dataset['h_errors']
    y = dataset['number_of_game']

    plot = sns.barplot(x=y, y=x)
    plot.get_figure().savefig('6_1_barplot.png')


def figure_2(dataset):
    plot = sns.barplot(x=dataset["number_of_game"],
                    y=dataset["length_minutes"],
                    hue=dataset["day_of_week"],
                    data=dataset)
    plot.get_figure().savefig('6_1_barplot_group.png')


def figure_3(dataset):
    plt.figure(figsize=(16, 6))
    heatmap = sns.heatmap(dataset.corr(), vmin=-1, vmax=1, annot=True, cmap='BrBG')
    heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':18}, pad=12)
    heatmap.get_figure().savefig('6_1_heatmap.png')


def figure_4(dataset):
    plot = sns.scatterplot(data=dataset, x="h_errors", y="h_walks")
    plot.set_title('scatterplot of h_errors, h_walks', fontdict={'fontsize':18}, pad=12)
    plot.get_figure().savefig('6_1_h_walks.png')

def figure_5(dataset):
    plt.figure(figsize=(10, 10))
    plt.title('day_of_week', fontsize=18)
    plot_data = dataset['day_of_week'].value_counts()
    plot_data.name = ''
    plot = plot_data.plot(kind='pie', fontsize=18, autopct='%1.0f%%')
    plot.get_figure().savefig('6_1_show.png')
figure_1(df)
figure_2(df)
figure_3(df)
figure_4(df)
figure_5(dataset)
