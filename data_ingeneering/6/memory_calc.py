import os
def memory_cal(data_file, dataset):
    file_size = os.path.getsize(data_file)
    print(f'Объем памяти, который занимает файл на диске: {file_size//1024:10} КБ')
    memory_usage_stat = dataset.memory_usage(deep=True)
    total_memory_usage = memory_usage_stat.sum()
    print(f'Объем памяти, который занимает набор данных при загрузке в память: {total_memory_usage//1024:10} КБ')
    column_stat = []
    for key in dataset.dtypes.keys():
        column_stat.append({
            "column_name": key,
            "memory_abs": memory_usage_stat[key] //1024,
            "memory_per": round(memory_usage_stat[key]/total_memory_usage *100, 4),
            "dtype": dataset.dtypes[key]
        })
    # Полученный набор данных отсортировать по занимаемому объему памяти.
    column_stat.sort(key = lambda x: x['memory_abs'], reverse=True)
    for column in column_stat:
        print(f"{column['column_name']:30}: {column['memory_abs']:10}КБ: {column['memory_per']:10}% : {column['dtype']}")
    return column_stat
