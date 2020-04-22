from tabula import read_pdf
import pandas as pd
import numpy as np
from copy import copy
from glob import glob


def standardize_cols(df, colnames, year):
    """
    Because the bank statements produced by tabula.read_pdf all have
    a different number of columns, this function ensures that they all
    have the same number of columns.

    Note that this function assumes that the 'Date' column has already been named.

    :param df: dataframe
    :param colnames: list of column names
    :param year: string that will be appended to Date col, which is mm/dd format
    :return:

    """
    # make a copy so that original dataset is unaffected by insert
    copy_df = copy(df)

    # insert columns if needed.  otherwise delete useless dataframe.
    if len(df.columns) > 5:
        copy_df = copy_df
        copy_df.columns = colnames
        copy_df['Date'] = copy_df['Date'] + f'/{year}'
        return copy_df
    elif len(df.columns) == 5:
        copy_df.insert(loc=1, column='Number', value=np.nan)
        copy_df.columns = colnames
        copy_df['Date'] = copy_df['Date'] + f'/{year}'
        return copy_df
    else:
        pass


def flatten_all_statements(statement_files_dir, colnames):
    """
    This function finds all PDF files inside a directory and– if they are valid
    Wells Fargo statement files– runs standardize_cols() func on them and
    flattens all statements into a single dataframe.

    :param statement_files_dir: String value for the name of the directory that contains
    Wells Fargo statement files
    :param colnames: list that contains column names for statement dataframes.
    :return:
    """
    statement_files = glob(f'./{statement_files_dir}/*.pdf')
    all_statements = []
    for file in statement_files:
        df_list = read_pdf(file,
                           pages='all',
                           silent=True,
                           encoding='utf-8',
                           pandas_options={'header': None})
        year = file.split('/')[3].split('-')[0]
        df_list = [standardize_cols(df, colnames, year) for df in df_list]
        df_list = pd.concat(df_list)
        all_statements.append(df_list)
    all_statements = pd.concat(all_statements)

    return all_statements


statements_dir = './StatementFiles/'
header = ['Date', 'Check Number', 'Description',
          'Inflow', 'Outflow', 'Balance']
all_dfs = flatten_all_statements(statements_dir, header)

# drop useless rows
dfs_2017 = all_dfs.dropna(subset=['Date'])
dfs_2017 = dfs_2017.dropna(subset=['Description'])
dfs_2017 = dfs_2017[dfs_2017['Description'] != 'Description']

# cast columns to useful data types
dfs_2017['Date'] = pd.to_datetime(dfs_2017['Date'])
dfs_2017['Date'] = dfs_2017['Date'].apply(lambda x: x.strftime('%Y/%m/%d'))
dfs_2017['Inflow'] = dfs_2017['Inflow'].str.replace(',', '').astype('float')
dfs_2017['Outflow'] = dfs_2017['Outflow'].str.replace(',', '').astype('float')
dfs_2017['Balance'] = dfs_2017['Balance'].str.replace(',', '').astype('float')
