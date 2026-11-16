"""Urgência/PII local → Groq dinâmica → Senado se aplicável."""
from privacy import minimal_context
from precheck import inspect_payload
from intent_routing import allowed_categories
from paths_validate import validate
from evidence import valid_source
from domains import LAWS
from groq_live import interpret
from senado_live import lookup
from texts import fallback
from results_live import futures_response

def stop(reason):
    result = fallback(reason)
    result.update(phase="F4", simulated=False)
    return result


async def explore_live(payload, key, transport):
    checked = inspect_payload(payload)
    if isinstance(checked, str):
        return stop(checked)
    topic, context = checked
    safe = minimal_context(topic, context)
    if not safe["concerns"]:
        return stop("general")
    allowed = allowed_categories(safe["concerns"])
    if not allowed:
        return stop("clarify")
    if not key:
        return stop("groq")
    try:
        answer = await interpret(safe, key, transport)
    except Exception:
        return stop("groq")
    if isinstance(answer, dict) and answer.get("result_kind") in {"clarify", "abstain"}:
        return stop("clarify")
    if not validate(answer, topic, allowed):
        return stop("json")
    category = answer["category"]
    if category not in LAWS:
        return futures_response(answer, concerns=safe["concerns"])
    try:
        source = await lookup(category, transport)
    except Exception:
        return futures_response(answer, source_failed=True, concerns=safe["concerns"])
    if not valid_source(source):
        return futures_response(answer, source_failed=True, concerns=safe["concerns"])
    return futures_response(answer, source, concerns=safe["concerns"])
