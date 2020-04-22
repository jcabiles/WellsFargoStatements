from tabula import read_pdf
import pandas as pd
import numpy as np
from copy import copy

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
    elif len(df.columns) == 5:
        copy_df.insert(loc=1, column='Number', value=np.nan)
        copy_df.columns = header
    else:
        copy_df = np.nan

    return copy_df

# create test DFs
header = ['Date', 'Check Number', 'Description',
          'Inflow', 'Outflow', 'Balance']
x = standardize_cols(rows[0], header)
y = standardize_cols(rows[1])
z = standardize_cols(rows[2])

# merge all DFs to one
july_dfs = pd.concat([x, y])
