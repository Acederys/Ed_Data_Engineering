import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
from sklearn.preprocessing import OrdinalEncoder # Импортируем Порядковое кодированиеот scikit-learn
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

# преобразовываем категориальные признаки в числовые
def transform_category():
    cat_columns = [] # создаем пустой список для имен колонок категориальных данных
    num_columns = [] # создаем пустой список для имен колонок числовых данных
    for column_name in dataset.columns: # смотрим на все колонки в датафрейме
        if (dataset[column_name].dtypes == 'category' or dataset[column_name].dtypes == 'bool'): # проверяем тип данных для каждой колонки
            cat_columns +=[column_name] # если тип объект - то складываем в категориальные данные
        else:
            num_columns +=[column_name] # иначе - числовые)
    ordinal = OrdinalEncoder()
    ordinal.fit(dataset[cat_columns])
    Ordinal_encoded = ordinal.transform(dataset[cat_columns])
    df_ordinal = pd.DataFrame(Ordinal_encoded, columns = cat_columns)
    df = pd.concat([dataset[num_columns], df_ordinal], axis=1)
    width = 2
    height = int(np.ceil(len(num_columns)/width))

    def fid_1():
        fig, ax = plt.subplots(nrows=height, ncols=width, figsize=(20,10)) # создаем "полотно", на котором будем "рисовать" графики
    #     ↑  более точная структура (почти синоним subplot). Говорим что у нас будет height строк и width столбцов
        for idx, column_name in enumerate(num_columns): # перебираем все числовые данные
            plt.subplot(height,width, idx+1) #берем конкретную ячейку из заранее подготовленную заготовку
                # рисуем с помощью библиотеки seaborn
            figure_1 =  sns.histplot(data=df, # какой датафрейм используем
                    x=column_name, # какую переменную отрисовываем
                    bins = 20);  # на сколько ячеек разбиваем
        return figure_1.get_figure().savefig(f'6_2_dearty.png')
    # fid_1()
    return df
df = transform_category()
# dataset.to_pickle('2_cat.pickle')
# Удаляем выбросы цены
del_index = df[(df['askPrice'] >= 80000) & (df['askPrice'] <= 2147483647)].index
df = df.drop(del_index)

def figure_2(dataset):
    g = plt.figure(figsize=(10,7))
    figure_2 = sns.histplot(data = dataset, # какой датафрейм используем
             x = 'askPrice', # какую переменную отрисовываем
             hue = 'isNew', # какую переменную используем для подкрашиваиния данных.
             bins = 15, # на сколько ячеек разбиваем
             kde = True, # чтобы отрисовал оценку плотности распределения
             palette='bwr'); # какую цветовую карту используем.
    return figure_2.get_figure().savefig(f'6_2_askPrice_isNew.png')



def figure_3(df):
    plt.figure(figsize=(16, 6))
    heatmap = sns.heatmap(df.corr(), vmin=-1, vmax=1, annot=True, cmap='BrBG')
    figure_3 = heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':18}, pad=12)
    return figure_3.get_figure().savefig('6_2_heatmap.png')


def figure_4(dataset):
    plot_3 = sns.boxplot(x=dataset["vf_Turbo"], y=dataset["askPrice"])
    return plot_3.get_figure().savefig('6_2_boxplot.png')


def figure_5(dataset):
    plt.figure(figsize=(16, 6))
    plt.title('isNew', fontsize=18)
    plot_data = dataset['isNew'].value_counts()
    plot_data.name = ''
    plot_5 = plot_data.plot(kind='pie', fontsize=18, autopct='%1.0f%%')
    return plot_5.get_figure().savefig('6_2_show.png')
# figure_2(df)
# figure_3(df)
# figure_4(df)
# figure_5(df)
