"""Consulta normas federais somente em referências pré-autorizadas."""
import asyncio
import json
import re
from datetime import date
from domains import LAWS

BASE = "https://legis.senado.leg.br/dadosabertos/legislacao/LEI"
URLS = {key: f"{BASE}/{num}/{year}.json" for key, (num, year) in LAWS.items()}
API = URLS["protection"]
PUBLIC = "https://legis.senado.gov.br/norma/572125"


def ementa(obj):
    if isinstance(obj, dict):
        for key, val in obj.items():
            if "ementa" in key.casefold() and isinstance(val, str) and len(val.strip()) >= 15:
                clean = re.sub(r"\s+", " ", val).strip()
                return clean if len(clean) <= 180 else clean[:177].rsplit(" ", 1)[0].rstrip(" ,;:.") + "…"
        return next((found for val in obj.values() if (found := ementa(val))), "")
    if isinstance(obj, list):
        return next((found for val in obj if (found := ementa(val))), "")
    return ""


async def lookup(category, transport):
    if category not in URLS:
        raise ValueError("Sem norma mapeada")
    response = await asyncio.wait_for(transport(URLS[category], method="GET", redirect="manual",
        headers={"Accept": "application/json"}), timeout=8)
    if response.status != 200:
        raise ValueError("Senado indisponível")
    raw = await response.text()
    if len(raw) > 300_000:
        raise ValueError("Resposta acima do limite")
    abstract = ementa(json.loads(raw))
    num, year = LAWS[category]
    if not abstract or not re.search(rf"(?<!\d){num}(?!\d)", raw.replace(".", "")) or str(year) not in raw:
        raise ValueError("Identificação e ementa não conferidas")
    return {"reference": f"Lei {num:,}/{year}".replace(",", "."),
            "title": abstract, "url": PUBLIC if category == "protection" else URLS[category],
            "checked_at": date.today().isoformat(), "simulated": False}
