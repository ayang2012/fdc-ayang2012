import pandas as pd


def transform(raw_df, ref_df):
    c_dict = {
        "#": "id",
        "Store": "restaurant",
        "Product Name": "name",
        "Ingredients on Product Page": "ingredients",
        "Allergens and Warnings": "allergens",
        "URL of primary product picture": "picture_url",
        "Fig Category 1": "category",
    }

    # Remove rows with missing product names and ingredients
    processed_df = raw_df.dropna(subset=["Product Name", "Ingredients on Product Page"])

    # Identify and store the removed rows
    removed_rows_df = raw_df[~raw_df.index.isin(processed_df.index)]

    # Output the number of removed rows
    print(f"{len(removed_rows_df)} rows removed, stored in debug_output/")
    removed_rows_df.to_csv("debug_output/dropped_df.csv", index=None)

    # Use category reference sheet to apply new categories
    df = pd.merge(
        ref_df,
        processed_df,
        left_on=["Restaurant name", "Restaurant original category"],
        right_on=["Store", "Product category"],
        how="right",
    )
    df = df[c_dict.keys()].rename(columns=c_dict)
    return df
