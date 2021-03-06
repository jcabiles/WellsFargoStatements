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
    :return: returns a Pandas dataframe
    """
    statement_files = glob(f'./{statement_files_dir}/2018*.pdf')
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


def cleanse_flattened_statements(statement_files_dir):
    """
    This function takes a dataframe of Wells Fargo bank statement records and
    cleans it by adding the correct header, getting rid of useless records (artifacts
    of processing from earlier functions), and casts columns to the correct datatype.

    :param statement_files_dir: takes dataframe produced by flatten_all_statements()
    :return: returns dataframe that only contains valid records
    """
    header = ['Date', 'Check Number', 'Description',
              'Inflow', 'Outflow', 'Balance']

    df = flatten_all_statements(statement_files_dir, header)

    # drop useless rows
    df = df.dropna(subset=['Date'])
    df = df.dropna(subset=['Description'])
    df = df[df['Description'] != 'Description']

    # cast columns to useful data types
    try:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y/%m/%d'))
        df['Inflow'] = df['Inflow'].str.replace(',', '').astype('float')
        df['Balance'] = df['Balance'].str.replace(',', '').astype('float')
    except pd.errors.ParserError as e:
        print(e)
        pass

    # cast as str first to prevent int values from being turned into NaN after str replace
    df['Outflow'] = df['Outflow'].astype('str')
    df['Outflow'] = df['Outflow'].str.replace(',', '').astype('float')

    # create column that combines inflow and outflow
    df['Cash Flow'] = np.where(df['Inflow'].isnull(),
                               df['Outflow'] * -1,
                               df['Inflow'])

    return df


# def main():
statements_dir = './StatementFiles/'
all_statements_df = cleanse_flattened_statements(statements_dir)
all_statements_df = all_statements_df.round(2)
all_statements_df.to_csv('2017-2020_statements.csv')


# if __name__ == "__main__":
#     main()
