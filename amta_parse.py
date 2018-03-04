from os import listdir
import tabula
import pandas as pd
import numpy as np
import tab_formatting


def parse_amta(path):
    df = tabula.read_pdf(path, java_options=["-Dfile.encoding=UTF8"], pages=[1,2], lattice=True, pandas_options={'error_bad_lines' : False})
    df = df.drop(df.index[14]).reset_index(drop=True)
    return tab_formatting.formatted_tab_df(df)


def fix_dtypes(tab_df):
    tab_df["Team"]["Number"].astype('int64')


# test_df = parse_amta('test.pdf')

tabs = list((filter(lambda x: x[-3:] == "pdf", listdir())))

with pd.ExcelWriter("tab-data.xlsx") as writer:
    lazy_counter = 0
    for tab in tabs:
        lazy_counter += 1
        parse_amta(tab).to_excel(writer, sheet_name=str(lazy_counter))


