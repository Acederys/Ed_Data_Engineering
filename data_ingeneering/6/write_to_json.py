import json
def write_to_json(column_stat,file):
    column_stat_json = column_stat.copy()
    # запись в json без применения оптимизации
    for column in column_stat_json:
        column['dtype'] = str(column['dtype'])
        column['memory_abs'] = int(column['memory_abs'])
        column['memory_per'] = float(column['memory_per'])
    with open(file, 'w', encoding='utf-8') as results:
        results.write(json.dumps(column_stat_json))
