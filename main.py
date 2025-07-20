from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from infrastructure.csv_annonce_repository import CsvAnnonceRepository
from infrastructure.sqlite_annonce_repository import SqliteAnnonceRepository
from application.stats_usecase import StatsUseCase
from application.add_annonce_usecase import AddAnnonceUseCase
from infrastructure.external.bienici_client import BieniciClient

# repo = CsvAnnonceRepository(path_csv="data/dataset_annonces.csv")
repo = SqliteAnnonceRepository(db_path="data/annonces.db")
stats_uc = StatsUseCase(repo)
client    = BieniciClient()
add_uc   = AddAnnonceUseCase(client, repo)

app = FastAPI(title="API MeilleureCopro", version="0.1.0")
templates = Jinja2Templates(directory="presentation/web/templates")

@app.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    dept_code: str | None = None,
    city:      str | None = None,
    zip_code:  str | None = None,
    url:       str | None = None
):
    stats, error = None, None
    try:
        if any((dept_code, city, zip_code)):
            stats = stats_uc.execute(dept_code, city, zip_code)
    except HTTPException as e:
        error = e.detail

    add_result, add_error = None, None
    try:
        if url:
            entity     = add_uc.execute(url)
            add_result = f"Annonce ajoutée : ID={entity.id}"
    except HTTPException as e:
        add_error = e.detail

    return templates.TemplateResponse("stats.html", {
        "request":     request,
        "stats":       stats,
        "error":       error,
        "filter":      {"dept_code": dept_code, "city": city, "zip_code": zip_code},
        "url": url,
        "add_result":  add_result,
        "add_error":   add_error
    })