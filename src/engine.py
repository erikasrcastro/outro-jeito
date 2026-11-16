"""Orquestra apenas o pré-processamento e mocks da F2."""
from safety import urgency
from privacy import TOPICS, has_identifiers, minimal_context
from evidence import valid_extraction, valid_source
from texts import fallback


def explore(payload, groq, senado):
    if not isinstance(payload, dict) or set(payload) - {"topic", "context"}:
        return fallback("invalid")
    topic, context = payload.get("topic"), payload.get("context", "")
    if not isinstance(context, str) or len(context) > 500:
        return fallback("invalid")
    if urgency(context) == "urgent":
        return fallback("urgent")  # nenhum provedor externo é chamado
    if not isinstance(topic, str) or topic not in TOPICS:
        return fallback("clarify")
    if has_identifiers(context):
        return fallback("privacy")  # bloqueia texto sem enviá-lo
    safe = minimal_context(topic, context)
    try:
        extraction = groq(safe)
    except Exception:
        return fallback("groq")
    if not valid_extraction(extraction) or extraction["topic"] != topic:
        return fallback("json")
    if extraction["result_kind"] != "map":
        return fallback("clarify")
    if topic != "direitos":
        return fallback("general")
    try:
        source = senado(extraction["category"])
    except Exception:
        return fallback("senado")
    if not valid_source(source):
        mock = isinstance(source, dict) and source.get("simulated") is True
        return fallback("preview" if mock else "senado")
    return {"status": "conditional", "evidence": "CONDITIONAL",
            "message": "Há uma referência legislativa; aplicação individual depende de condições.",
            "source": {key: source[key] for key in ("reference", "title", "url", "checked_at")},
            "primary_action": {"id": "open_official_source", "label": "Consultar a fonte"},
            "secondary_action": {"id": "return_home", "label": "Escolher outro assunto"},
            "phase": "F2", "simulated": False}
