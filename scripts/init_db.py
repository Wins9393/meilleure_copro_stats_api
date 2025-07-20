import pandas as pd
from sqlalchemy import create_engine

CSV_PATH = "data/dataset_annonces.csv"
DB_PATH  = "data/annonces.db"

def main():
    engine = create_engine(f"sqlite:///{DB_PATH}")

    df = pd.read_csv(CSV_PATH)
    df.columns = [c.strip().lower() for c in df.columns]
    df = df[[
        "id",
        "dept_code",
        "city",
        "zip_code",
        "condominium_expenses"
    ]]

    df.to_sql("annonces", engine, if_exists="replace", index=False)
    print(f"Import CSV → SQLite terminé ({len(df)} lignes) dans {DB_PATH}")

if __name__ == "__main__":
    main()