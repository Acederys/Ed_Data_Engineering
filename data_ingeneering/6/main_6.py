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


#Используя оптимизированный набор данных,
# построить пять-семь графиков
# (включая разные типы: линейный, столбчатый,
# круговая диаграмма, корреляция и т.д.)
# столбчатый
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

df.to_pickle('6.pickle')
#
# utem = df[(df['sigma_q'] >= 250) & (df['sigma_q'] <= 126130.0)].index
# df= df.drop(utem)
# utem_2 = df[(df['diameter'] >= 10) & (df['diameter'] <= 939.4)].index
# df= df.drop(utem_2)
# utem_3 = df[(df['albedo'] <= 0.6)].index
# df= df.drop(utem_3)
DF_cat= pd.DataFrame
utem = df[df['year'] <= 2000].index
DF_cat = df.drop(utem)
utem_1 = DF_cat[DF_cat['year'] >= 2005].index
DF_cat = DF_cat.drop(utem_1)
def figure_1(df):
    figure_1 = sns.boxplot(x=df['year'], y=df["timbre_avg_0"]);
    return figure_1.get_figure().savefig(f'6_6_boxplot.png')

def figure_2(df):
    g = plt.figure(figsize=(10,7))
    figure_2 = sns.histplot(data = df, # какой датафрейм используем
             x = 'timbre_avg_1', # какую переменную отрисовываем
             hue = 'year', # какую переменную используем для подкрашиваиния данных.
             bins = 15, # на сколько ячеек разбиваем
             kde = True, # чтобы отрисовал оценку плотности распределения
             palette='bwr'); # какую цветовую карту используем.
    return figure_2.get_figure().savefig(f'6_6_histplot.png')

def figure_3(df):
    plt.figure(figsize=(15,6)) # создаем "полотно", уточняем размер
    figure_3 = sns.histplot(data=df, # какой датафрейм используем
             x='year', # какую переменную отрисовываем
             bins = 20, # на сколько ячеек разбиваем
             ); # захотели использовать логарифмический масштаб (для очень больших диапазонов)
    return figure_3.get_figure().savefig(f'6_6_histplot_response_url.png')

def figure_4(df):
    figure_4 = sns.heatmap(df.corr(), cmap="Blues")
    return figure_4.get_figure().savefig(f'6_6_heatmap.png')


def figure_5(dataset):
    plt.figure(figsize=(16, 6))
    plt.title('year', fontsize=18)
    plot_data = dataset['year'].value_counts()
    plot_data.name = ''
    plot_5 = plot_data.plot(kind='pie', fontsize=18, autopct='%1.0f%%')
    return plot_5.get_figure().savefig('6_6_show.png')
# figure_1(DF_cat)
# figure_2(DF_cat)
# figure_3(df)
# figure_4(df)
figure_5(DF_cat)
