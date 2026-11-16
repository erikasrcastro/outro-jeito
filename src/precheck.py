"""Antes de qualquer consulta, filtra risco, entrada e identificadores."""
from privacy import TOPICS, has_identifiers
from safety import urgency


def inspect_payload(payload):
    if not isinstance(payload, dict) or set(payload) - {"topic", "context"}:
        return "invalid"
    topic, context = payload.get("topic"), payload.get("context", "")
    if not isinstance(context, str) or len(context) > 500:
        return "invalid"
    if urgency(context) == "urgent":
        return "urgent"
    if not isinstance(topic, str) or topic not in TOPICS:
        return "clarify"
    if has_identifiers(context):
        return "privacy"
    return topic, context
