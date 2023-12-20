import pandas as pd
"""
downcast:
        - 'integer' or 'signed':smallest signed int dtype (min.:np.int8)
        - 'unsigned':smallest signed int dtype (min.:np.uint8)
        - 'float':smallest signed int dtype (min.:np.float32)
"""
def col_num_int(dataset):
    dataset_int = dataset.select_dtypes(include=['int'])
    converted_int = dataset_int.apply(pd.to_numeric, downcast = 'unsigned')
    return converted_int

def col_num_float(dataset):
    dataset_int = dataset.select_dtypes(include=['float'])
    converted_float = dataset_int.apply(pd.to_numeric, downcast = 'float')
    return converted_float
