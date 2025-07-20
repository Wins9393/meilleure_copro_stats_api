import pandas as pd
from typing import Any, Dict

class CsvAnnonceRepository:
    def __init__(self, path_csv: str):
        self.path_csv = path_csv
        self.df = pd.read_csv(path_csv, dtype={"ZIP_CODE": str})
        self.df.columns = [c.strip().lower() for c in self.df.columns]
        self.df["zip_code"] = self.df["zip_code"].str.zfill(5)

    def filter(
        self,
        dept_code: str | None = None,
        city: str | None = None,
        zip_code: str | None = None
    ) -> pd.DataFrame:
        df = self.df

        if dept_code:
            df = df[df["dept_code"].astype(str) == dept_code]
        if city:
            df = df[df["city"].str.lower() == city.lower()]
        if zip_code:
            df = df[df["zip_code"] == zip_code]

        return df
    
    def add(self, annonce: Dict[str, Any]) -> None:
        row = {col: annonce.get(col) for col in self.df.columns}
        new_df = pd.DataFrame([row])

        self.df = pd.concat([self.df, new_df], ignore_index=True)
        self.df.to_csv(self.path_csv, index=False)