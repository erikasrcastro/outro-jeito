"""Somente F2: nunca confundir simuladores com fontes reais."""


def groq(safe_payload):
    return {"topic": safe_payload["topic"], "category": "rights_information",
            "result_kind": "map"}


def senado(category):
    return {"simulated": True, "category": category}
