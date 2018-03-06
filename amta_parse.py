from os import listdir
import tabula
import pandas as pd
import tab_formatting
import re

def fix_page(page_df):
    if page_df.shape[1] == 13:
        page_df.drop(columns=['Unnamed: 0', 'Unnamed: 2', 'Unnamed: 4', 'Unnamed: 6', 'Unnamed: 8', 'Unnamed: 10', 'Unnamed: 12'], inplace=True)

def parse_amta(path):
    p1 = tabula.read_pdf(path, java_options=["-Dfile.encoding=UTF8"], pages=[1], lattice=True, pandas_options={'error_bad_lines' : False})
    p2 = tabula.read_pdf(path, java_options=["-Dfile.encoding=UTF8"], pages=[2], lattice=True, pandas_options={'error_bad_lines' : False})
    fix_page(p1)
    fix_page(p2)
    df = pd.concat([p1,p2], ignore_index=True)
    try:
        df = df.drop(df.index[14]).reset_index(drop=True)
    except IndexError:
        print("Skipped "+ path)
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


