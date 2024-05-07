from fig_data_challenge.etl import transform
import pandas as pd
from pandas.testing import assert_frame_equal

INPUT_EXCEL_PATH = "data/restaurant_data.xlsx"


def test_transform():
    test_file_path = "src/tests/test_data/df_raw_sample_10_42.csv"
    test_result_path = "src/tests/test_data/df_raw_sample_10_42_result.csv"
    test_df = pd.read_csv(test_file_path)
    ref_df = pd.read_excel(INPUT_EXCEL_PATH, sheet_name="Reference categories")
    df = transform.transform(test_df, ref_df).reset_index(drop=True)
    result_df = pd.read_csv(test_result_path)
    assert_frame_equal(df, result_df)
