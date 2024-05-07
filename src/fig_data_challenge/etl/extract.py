import pandas as pd

INPUT_EXCEL_PATH = "data/restaurant_data.xlsx"


def extract():
    df = pd.read_excel(INPUT_EXCEL_PATH, sheet_name="Restaurant Menu Items")
    ref_df = pd.read_excel(INPUT_EXCEL_PATH, sheet_name="Reference categories")
    return df, ref_df
