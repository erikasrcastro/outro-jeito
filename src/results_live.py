"""Separa norma consultada de hipóteses; protege cenários de moradia."""
from local_guides import GUIDES
from property_paths import PATHS


def futures_response(extraction, source=None, source_failed=False, concerns=()):
    sensitive = "property_split" in concerns
    guide = "protection" if sensitive else extraction["category"]
    _, url, label = GUIDES[guide]
    verified = bool(source)
    origin = source if verified else {"url": url, "source_kind": "official_guide"}
    caveat = (f"A referência legislativa {source['reference']} foi consultada; isso não "
              "confirma sua aplicação a uma situação individual." if verified else
              "Não foi possível verificar a referência legislativa no Senado nesta consulta." if source_failed else
              "As alternativas não foram verificadas para uma situação individual.")
    message = ("Você não precisa decidir tudo agora. Conheça os caminhos no seu ritmo. "
               + caveat)
    paths = PATHS if sensitive else extraction["paths"]
    return {"status": "futures", "phase": "F4", "simulated": False,
            "evidence": "CONDITIONAL" if verified else "UNVERIFIED" if source_failed else "HYPOTHESIS",
            "message": message,
            "paths": [{**item, "evidence": "HYPOTHESIS"} for item in paths],
            "source": origin, "source_verified": verified,
            "primary_action": {"id": "open_official_source", "label": "Ver fonte e condições" if verified else label},
            "secondary_action": {"id": "choose_topic", "label": "Explorar outro assunto"}}
