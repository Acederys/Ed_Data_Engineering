import pandas as pd
def mem_usage(pandas_obj):
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else:
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b/1024 ** 2
    return "{:03.2f} MB".format(usage_mb)
def col_category(dataset):
    converted_odj = pd.DataFrame()
    #Преобразовать все колонки с типом данных «object» в категориальные,
    # если количество уникальных значений колонки составляет менее 50%.
    dataset_obj = dataset.select_dtypes(include = ['object']).copy()
    for col in dataset_obj.columns:
        num_unique_values = len(dataset_obj[col].unique())
        num_total_value = len(dataset_obj[col])
        if num_unique_values/num_total_value < 0.5:
            converted_odj.loc[:, col] = dataset_obj[col].astype('category')
        else:
            converted_odj.loc[:, col] = dataset_obj[col]
    return converted_odj
