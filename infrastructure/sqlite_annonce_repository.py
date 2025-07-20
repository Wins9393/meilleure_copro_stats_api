import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text
from typing import Any, Dict, Optional

class SqliteAnnonceRepository:
    def __init__(self, db_path: str = "data/annonces.db"):
        self.db_path = Path(db_path)
        self.engine = create_engine(
            f"sqlite:///{self.db_path}",
            connect_args={"check_same_thread": False}
        )

    def filter(
        self,
        dept_code: Optional[str] = None,
        city:      Optional[str] = None,
        zip_code:  Optional[str] = None
    ) -> pd.DataFrame:
        
        clauses = []
        params = {}

        if dept_code:
            clauses.append("dept_code = :dept_code")
            params["dept_code"] = dept_code

        if city:
            clauses.append("LOWER(city) = :city")
            params["city"] = city.lower()

        if zip_code:
            clauses.append("zip_code = :zip_code")
            params["zip_code"] = zip_code

        where = " AND ".join(clauses) if clauses else "1=1"
        sql = f"""
            SELECT condominium_expenses
            FROM annonces
            WHERE {where}
        """
        df = pd.read_sql_query(sql, self.engine, params=params)
        return df

    def add(self, annonce: Dict[str, Any]) -> None:
        sql = text("""
            INSERT OR REPLACE INTO annonces
            (id, dept_code, city, zip_code, condominium_expenses)
            VALUES (:id, :dept_code, :city, :zip_code, :condominium_expenses)
        """)
        params = {k: annonce.get(k) for k in (
            "id", "dept_code", "city", "zip_code", "condominium_expenses"
        )}
        with self.engine.begin() as conn:
            conn.execute(sql, params)