import numpy as np
import pandas as pd


file_path = "data.csv"
copy_path = "copy.csv"
save_path = "save.csv"
comment_symbol = '#'
split_symbol = ';'
header_line = 0


def extract_comments(old, new, symbol):
    try:
        with open(new, 'w') as new_file, open(old, 'r') as old_file:
            for line in old_file:
                new_line = line.replace(" ", "")
                if new_line[0] == symbol:
                    new_file.write(line)
    except FileNotFoundError as err:
        print(err)
    except PermissionError as err:
        print(err)


def read_data(path):
    data = []

    try:
        data = pd.read_csv(path, comment=comment_symbol, header=header_line, sep=split_symbol)
    except FileNotFoundError as err:
        print(err)
    except UnicodeDecodeError as err:
        print(err)
    except ValueError as err:
        print(err)

    return data


def replace_values(data, to_symbol, from_symbol):
    try:
        result = data.replace(to_replace=to_symbol, value=from_symbol)
    except NameError as err:
        print(err)

    return result


def initial_data_frame(path):
    data = read_data(path)
    data.columns.array[0] = 'ID'
    o = data.columns
    data = replace_values(data, '', np.nan)

    data['ID'] = data['ID'].apply(int)
    return data


def sort_records(data, key):
    return data.sort_values(by=[key])


def delete_empty_variety(data):
    return data.dropna()


def replace_nan_to_median(data):
    column_names = data.columns

    for col in column_names:
        current_col = data[col]
        dtype = current_col.dtype

        if dtype == 'int64':
            m = current_col.median()
        else:
            m = current_col.value_counts().max()

        data[col] = current_col.fillna(value=m)

    return data


def replace_column_names(data, to_symbol, from_symbol):
    column_names = data.columns
    result = []

    for col in column_names:
        result.append(col.replace(from_symbol, to_symbol))
    data.columns = result

    return data


def save_without_index(data, path):
    data.to_csv(path, index=False, sep=',')


if __name__ == '__main__':
    # extract_comments(file_path, copy_path, comment_symbol)

    data = initial_data_frame(file_path)
    data = sort_records(data, 'ID')

    # data = delete_empty_variety(data)

    data = replace_nan_to_median(data)
    data = replace_column_names(data, '_', '.')

    # save_without_index(data, save_path)

    print(data)
