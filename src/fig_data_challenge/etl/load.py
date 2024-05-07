import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, ForeignKey


def connect_to_database(db_url):
    """Establish connection to the database."""
    engine = create_engine(db_url)
    return engine


def define_table_schema(metadata):
    """Define table schema."""
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


def create_tables(metadata, engine):
    """Create tables."""
    metadata.create_all(engine)


def write_table_to_database(engine, df, table_name, id_column):
    """Write DataFrame to a database table."""
    # Write data to the table
    existing_records = pd.read_sql(f"SELECT * FROM {table_name}", engine)
    new_records = df[~df[id_column].isin(existing_records[id_column])]
    new_records.to_sql(name=table_name, con=engine, if_exists="append", index=False)


def write_to_database(engine, df):
    """Write to database."""
    # Write restaurants data
    restaurant_df = (
        pd.DataFrame(df["restaurant"].unique(), columns=["name"])
        .reset_index()
        .rename(columns={"index": "id"})
    )
    write_table_to_database(engine, restaurant_df, "restaurants", "id")

    # Write products data
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
    write_table_to_database(engine, product_df, "products", "id")


def load(df, db_url):
    """Load data into the database."""
    engine = connect_to_database(db_url)
    metadata = sqlalchemy.MetaData()
    define_table_schema(metadata)
    create_tables(metadata, engine)
    engine = engine.raw_connection()
    write_to_database(engine, df)
