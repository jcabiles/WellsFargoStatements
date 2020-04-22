from tabula import read_pdf
import pandas as pd
import numpy as np
from copy import copy
from glob import glob

statement_file = './StatementFiles/2017-07.pdf'
rows = read_pdf(statement_file,
                pages='all',
                silent=True,
                encoding='utf-8',
                pandas_options={'header': None})


def standardize_cols(df, header):
    """
    Because the bank statements produced by tabula.read_pdf all have
    a different number of columns, this function ensures that they all
    have the same number of columns.

    :param df: dataframe
    :param header: list of column names
    :return:

    """
    # make a copy so that original dataset is unaffected by insert
    copy_df = copy(df)

    # insert columns if needed.  otherwise delete useless dataframe.
    if len(df.columns) > 5:
        copy_df = copy_df
        copy_df.columns = header
        return copy_df
    elif len(df.columns) == 5:
        copy_df.insert(loc=1, column='Number', value=np.nan)
        copy_df.columns = header
        return copy_df
    else:
        pass


# create test DFs
header = {'Date', 'Check Number', 'Description',
          'Inflow', 'Outflow', 'Balance'}


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
        df_list = read_pdf(statement_file,
                           pages='all',
                           silent=True,
                           encoding='utf-8',
                           pandas_options={'header': None})
        df_list = [standardize_cols(df, colnames) for df in df_list]
        df_list = pd.concat(df_list)
        all_statements.append(df_list)
    all_statements = pd.concat(all_statements)

    return all_statements


statements_dir = './StatementFiles/'
list_dfs = flatten_all_statements(statements_dir)