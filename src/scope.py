"""Temas fora da norma mapeada: orientação honesta sem consulta externa."""
import re
from safety import normalize
from texts import fallback

GUIDES = {
    "custody": "https://www.cnj.jus.br/poder-judiciario/defensoria-publica/",
    "work": "https://www.gov.br/pt-br/servicos/buscar-emprego-no-sistema-nacional-de-emprego-sine",
}


def scope_response(context):
    value = normalize(context)
    if re.search(r"\b(guarda|custodia)\b", value) and re.search(r"\b(filho|filhos|crianca|menor)\b", value):
        kind = "custody"
    elif re.search(r"\b(trabalho|emprego|desemprego|vaga|renda)\b", value):
        kind = "work"
    else:
        return None
    result = fallback(kind)
    result.update(phase="F3", simulated=False, source={"url": GUIDES[kind]})
    return result
