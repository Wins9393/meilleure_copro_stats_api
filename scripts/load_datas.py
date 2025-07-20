import requests, tarfile, os
from io import BytesIO

url = "https://storage.googleapis.com/data.meilleurecopro.com/stage/dataset_annonces.csv.tar.gz"
resp = requests.get(url)
resp.raise_for_status()

os.makedirs("data", exist_ok=True)
with tarfile.open(fileobj=BytesIO(resp.content), mode="r:gz") as tar:
    tar.extractall(path="data")

print("Fichiers extraits dans ./data/")