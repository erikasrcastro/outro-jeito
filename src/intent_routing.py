"""Relação fechada entre pistas locais e domínio de consulta permitido."""
from domains import candidates

SPECIAL = {"reporting": "protection", "financial_control": "justice",
           "custody_concern": "family", "property_split": "family"}


def allowed_categories(concerns):
    matched = set(candidates(concerns))
    focus = {SPECIAL[tag] for tag in concerns if tag in SPECIAL}
    if len(focus) > 1:
        return set()
    if focus:
        chosen = next(iter(focus))
        extras = matched - {chosen}
        if chosen == "family" and "property_split" in concerns:
            extras.discard("housing")
        if chosen == "family" and "custody_concern" in concerns:
            extras.discard("children")
        if chosen == "justice" and "financial_control" in concerns:
            extras.discard("work")
        if extras:
            return set()
        return {chosen}
    return matched if len(matched) == 1 else set()
