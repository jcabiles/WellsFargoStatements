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
colnames = ['Date', 'Check Number', 'Description',
            'Inflow', 'Outflow', 'Balance']

# merge all DFs to one
july_dfs = [standardize_cols(row, colnames) for row in rows]
july_dfs = pd.concat(july_dfs)


# iterate over directory to find and pr
# ocess all PDF files
def loop_statement_files(statement_files_dir):
    statements_dir = statement_files_dir
    statement_files = glob(f'./{statement_files_dir}/*.pdf')
    all_statements = []
    for file in statement_files:
        df_list = read_pdf(statement_file,
                           pages='all',
                           silent=True,
                           encoding='utf-8',
                           pandas_options={'header': None})
        all_statements.append(df_list)
    return all_statements


statements_dir = './StatementFiles/'
list_dfs = loop_statement_files(statements_dir)