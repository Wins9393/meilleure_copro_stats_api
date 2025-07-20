from domain.services import calcul_stats
from infrastructure.csv_annonce_repository import CsvAnnonceRepository
from fastapi import HTTPException

class StatsUseCase:
    def __init__(self, repo: CsvAnnonceRepository):
        self.repo = repo

    def execute(self,
                dept_code: str | None = None,
                city:      str | None = None,
                zip_code:  str | None = None
    ) -> dict:
        df = self.repo.filter(dept_code=dept_code, city=city, zip_code=zip_code)
        if df.empty:
            raise HTTPException(status_code=404, detail="Aucune annonce pour ces critères")
        stats = calcul_stats(df)
        return {
            "filtre": {
                "dept_code": dept_code,
                "city":      city,
                "zip_code":  zip_code
            },
            **stats
        }