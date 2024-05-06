import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, ForeignKey


def extract():
    excel_file = "data/restaurant_data.xlsx"
    df = pd.read_excel(excel_file, sheet_name="Restaurant Menu Items")
    ref_df = pd.read_excel(excel_file, sheet_name="Reference categories")
    return df, ref_df


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


def load(df):
    # Connection URL for SQLite database
    db_url = "sqlite:///fdc_db.db"

    # Create a SQLAlchemy engine
    engine = create_engine(db_url)

    # Define table schema
    metadata = sqlalchemy.MetaData()

    restaurant_table = sqlalchemy.Table(
        "restaurants",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("name", sqlalchemy.String),
    )

    product_table = sqlalchemy.Table(
        "products",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("name", sqlalchemy.String),
        sqlalchemy.Column("ingredients", sqlalchemy.String),
        sqlalchemy.Column("allergens", sqlalchemy.String),
        sqlalchemy.Column("picture_url", sqlalchemy.String),
        sqlalchemy.Column("category", sqlalchemy.String),
        sqlalchemy.Column(
            "restaurant_id", sqlalchemy.Integer, ForeignKey("restaurants.id")
        ),
    )

    # Create tables
    metadata.create_all(engine)

    # Write to database excluding duplicates
    engine = engine.raw_connection()

    restaurant_df = (
        pd.DataFrame(df["restaurant"].unique(), columns=["name"])
        .reset_index()
        .rename(columns={"index": "id"})
    )
    existing_records = pd.read_sql("SELECT * FROM restaurants", engine)
    new_records = restaurant_df[~restaurant_df["id"].isin(existing_records["id"])]
    new_records.to_sql(name="restaurants", con=engine, if_exists="append", index=False)

    query = "SELECT * FROM restaurants"
    restaurants_tb = pd.read_sql(query, engine)

    product_columns = [
        "id",
        "name_x",
        "ingredients",
        "allergens",
        "picture_url",
        "category",
        "restaurant_id",
    ]
    product_df = df.merge(
        restaurants_tb.rename(columns={"id": "restaurant_id"}),
        left_on="restaurant",
        right_on="name",
    )[product_columns]
    product_df.rename(
        columns={"name_x": "name", "product_category": "category"}, inplace=True
    )
    existing_records = pd.read_sql("SELECT * FROM products", engine)
    new_records = product_df[~product_df["id"].isin(existing_records["id"])]
    new_records.to_sql(name="products", con=engine, if_exists="append", index=False)


if __name__ == "__main__":
    df, ref_df = extract()
    df = transform(df, ref_df)
    df.to_csv("new.csv", index=None)
    load(df)
