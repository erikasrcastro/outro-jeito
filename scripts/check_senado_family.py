"""Diagnóstico público da API Senado: sem chave ou relato pessoal."""
import json
from urllib.request import Request, urlopen

URL = "https://legis.senado.leg.br/dadosabertos/legislacao/LEI/10406/2002.json"
try:
    with urlopen(Request(URL, headers={"Accept": "application/json"}), timeout=20) as response:
        content = response.read(200_001)
        print("HTTP:", response.status)
        print("Content-Type:", response.headers.get("Content-Type"))
        print("Bytes amostrados:", len(content), "| Limite do adapter: 200000")
        text = content.decode("utf-8", errors="replace")
        print("Número 10406 encontrado:", "10406" in text.replace(".", ""))
        print("Ano 2002 encontrado:", "2002" in text)
        print("Campo ementa mencionado:", "ementa" in text.casefold())
        if len(content) <= 200_000:
            value = json.loads(text)
            print("JSON:", type(value).__name__)
except Exception as exc:
    print("Falha:", type(exc).__name__, str(exc)[:180])
