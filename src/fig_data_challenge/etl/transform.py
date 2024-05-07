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

    # remove no product names
    df = raw_df[raw_df["Product Name"].notna()]
    df = df[df["Ingredients on Product Page"].notna()]
    print(f"{raw_df.shape[0]-df.shape[0]} rows removed")

    # Use category reference sheet to apply new categories
    df = pd.merge(
        ref_df,
        df,
        left_on=["Restaurant name", "Restaurant original category"],
        right_on=["Store", "Product category"],
        how="right",
    )
    df = df[c_dict.keys()].rename(columns=c_dict)
    return df
