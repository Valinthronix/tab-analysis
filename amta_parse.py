import tabula
import pandas as pd
import numpy as np
import tab_formatting


def parse_amta(path):
    df = tabula.read_pdf(path, java_options=["-Dfile.encoding=UTF8"], pages=[1,2], lattice=True)
    df = df.drop(df.index[14]).reset_index(drop=True)
    return tab_formatting.formatted_tab_df(df)

def fix_dtypes(tab_df):
    tab_df["Team"]["Number"].astype('int64')


def tab_df_to_excel(tab_df):
    tab_df.to_excel("test.xlsx")

test_df = parse_amta('test.pdf')
tab_df_to_excel(test_df)