from fastapi import HTTPException
from urllib.parse import urlparse, parse_qs

from infrastructure.external.bienici_client import BieniciClient
from infrastructure.csv_annonce_repository import CsvAnnonceRepository
from domain.entities import Annonce

class AddAnnonceUseCase:
    def __init__(self,
                 client: BieniciClient,
                 repo:   CsvAnnonceRepository):
        self.client = client
        self.repo   = repo

    def execute(self, url: str) -> Annonce:
        annonce_id = self._extract_id(url)

        try:
            data = self.client.fetch(annonce_id)
        except Exception as e:
            raise HTTPException(status_code=502,
                                detail=f"Erreur lors de l'appel à Bienici : {e}")

        try:
            entity = Annonce(
                id                     = str(data["id"]),
                dept_code              = str(data["departmentCode"]),
                city                   = str(data["city"]),
                zip_code               = str(data["postalCode"]),
                condominium_expenses   = float(data["annualCondominiumFees"])
            )
        except KeyError as e:
            raise HTTPException(status_code=502,
                                detail=f"Clé manquante dans le JSON Bienici : {e}")

        self.repo.add(entity.dict())

        return entity

    def _extract_id(self, url: str) -> str:
        parsed = urlparse(url)
        path = parsed.path
        
        segment = path.rstrip("/").split("/")[-1]
        
        if not segment:
            raise HTTPException(
                status_code=400,
                detail="Impossible d'extraire l'id de l'URL fournie"
            )
        
        return segment