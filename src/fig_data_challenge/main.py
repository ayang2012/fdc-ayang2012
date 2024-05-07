from fig_data_challenge.etl import extract, transform, load

if __name__ == "__main__":
    db_url = "sqlite:///fdc_db.db"
    df, ref_df = extract.extract()
    df = transform.transform(df, ref_df)
    load.load(df, db_url)
