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