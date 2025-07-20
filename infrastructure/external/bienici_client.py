import httpx

class BieniciClient:
    BASE_URL = "https://www.bienici.com/realEstateAd.json"

    def fetch(self, annonce_id: str) -> dict:
        resp = httpx.get(self.BASE_URL, params={"id": annonce_id}, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()

        return data.get("data", {}).get("realEstateAd", data)