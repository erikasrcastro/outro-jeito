"""Separa fontes checadas de ideias, sempre em linguagem simples."""
from local_guides import GUIDES
from property_paths import PATHS


def futures_response(extraction, source=None, source_failed=False, concerns=()):
    sensitive = "property_split" in concerns
    guide = "protection" if sensitive else extraction["category"]
    _, url, label = GUIDES[guide]
    verified = bool(source)
    origin = source if verified else {"url": url, "source_kind": "official_guide"}
    caveat = (f"Consultei a {source['reference']} no Senado. A lei existe, mas isso não "
              "quer dizer que vale para a sua situação." if verified else
              "Não consegui conferir a lei no Senado agora. Não vou afirmar que "
              "ela vale para você." if source_failed else
              "Não consultei uma lei sobre este assunto. Isso ainda não foi confirmado.")
    message = "Você não precisa decidir tudo agora. Estas são ideias, não promessas. " + caveat
    paths = PATHS if sensitive else extraction["paths"]
    return {"status": "futures", "phase": "F4", "simulated": False,
            "evidence": "CONDITIONAL" if verified else "UNVERIFIED" if source_failed else "HYPOTHESIS",
            "message": message,
            "paths": [{**item, "evidence": "HYPOTHESIS"} for item in paths],
            "source": origin, "source_verified": verified,
            "primary_action": {"id": "open_official_source", "label": "Entender a lei" if verified else label},
            "secondary_action": {"id": "choose_topic", "label": "Ver outro assunto"}}
