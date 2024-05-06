from fig_data_challenge.main import transform
import pandas as pd
from pandas.testing import assert_frame_equal


def test_transform():
    test_df = pd.read_csv("src/tests/test_data/df_raw_sample_10_42.csv")
    df = transform(test_df).reset_index(drop=True)
    result_df = pd.read_csv("src/tests/test_data/df_raw_sample_10_42_result.csv")
    assert_frame_equal(df, result_df)
