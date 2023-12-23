import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import seaborn as sns
from sklearn.preprocessing import OrdinalEncoder # Импортируем Порядковое кодированиеот scikit-learn
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

def transform_category():
    cat_columns = [] # создаем пустой список для имен колонок категориальных данных
    num_columns = [] # создаем пустой список для имен колонок числовых данных
    for column_name in dataset.columns: # смотрим на все колонки в датафрейме
        if (dataset[column_name].dtypes == 'category' or dataset[column_name].dtypes == 'bool' or dataset[column_name].dtypes == 'object'): # проверяем тип данных для каждой колонки
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

utem = df[(df['address_lng'] <= 0)].index
df = df.drop(utem)
utem_1 = df[(df['address_lat'] <= 0)].index
df= df.drop(utem_1)

def figure_1(df):
    figure_1 =  sns.boxplot(x=df["employment_name"], y=df["address_street"])
    return figure_1.get_figure().savefig(f'6_4_boxplot.png')

def figure_2(df):
    g = plt.figure(figsize=(10,7))
    figure_2 = sns.histplot(data = df, # какой датафрейм используем
             x = 'response_url', # какую переменную отрисовываем
             hue = 'accept_kids', # какую переменную используем для подкрашиваиния данных.
             bins = 15, # на сколько ячеек разбиваем
             kde = True, # чтобы отрисовал оценку плотности распределения
             palette='bwr'); # какую цветовую карту используем.
    return figure_2.get_figure().savefig(f'6_4_histplot.png')

def figure_3(df):
    plt.figure(figsize=(15,6)) # создаем "полотно", уточняем размер
    figure_3 = sns.histplot(data=df, # какой датафрейм используем
             x='employment_name', # какую переменную отрисовываем
             bins = 20, # на сколько ячеек разбиваем
             ); # захотели использовать логарифмический масштаб (для очень больших диапазонов)
    return figure_3.get_figure().savefig(f'6_4_histplot_response_url.png')

def figure_4(df):
    figure_4 = sns.heatmap(df.corr(), cmap="Blues")
    return figure_4.get_figure().savefig(f'6_4_heatmap.png')


def figure_5(dataset):
    plt.figure(figsize=(16, 6))
    plt.title('archived', fontsize=18)
    plot_data = dataset['archived'].value_counts()
    plot_data.name = ''
    plot_5 = plot_data.plot(kind='pie', fontsize=18, autopct='%1.0f%%')
    return plot_5.get_figure().savefig('6_4_show.png')
figure_1(df)
# figure_2(df)
# figure_3(dataset)
# figure_4(df)
# figure_5(dataset)

