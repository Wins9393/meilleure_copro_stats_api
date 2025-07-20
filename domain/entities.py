from pydantic import BaseModel

class Annonce(BaseModel):
    id: str
    dept_code: str
    city: str
    zip_code: str
    condominium_expenses: float