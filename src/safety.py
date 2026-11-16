"""Triagem local preliminar; nenhuma ausência de gatilho prova segurança."""
import re
import unicodedata

STRONG = (
    r"\bsocorro\b", r"\bme trancou\b", r"\best(a|ao) armado(s)?\b",
    r"\b(esta|ta) me agredindo\b", r"\b(vai|quer) me matar\b",
    r"\bnao consigo (respirar|sair)\b", r"\bsangramento intenso\b",
    r"\bme ameacando agora\b", r"\b(vou|quero) me matar\b",
)
UNCERTAIN = ("medo", "ameac", "agred", "perigo", "violenc", "controla")
QUOTED = ("li uma noticia", "num filme", "em um filme", "numa serie", "era uma citacao", "no livro")
DENIAL = (r"\bnao (estou|ha|tem|existe) (em )?perigo\b", r"\bnao (estou|sou) (sendo )?agredid")


def normalize(value):
    plain = unicodedata.normalize("NFD", value.casefold())
    return "".join(c for c in plain if unicodedata.category(c) != "Mn")


def urgency(text):
    value = normalize(text)
    matches = [p for p in STRONG if re.search(p, value)]
    if "nao esta armado" in value or "nao ta armado" in value:
        matches = [p for p in matches if "armado" not in p]
    if "nao me trancou" in value:
        matches = [p for p in matches if "trancou" not in p]
    current = ("me agredindo", "nao consigo respirar", "sangramento intenso", "me trancou")
    if matches and not (any(x in value for x in QUOTED) and
                        not any(x in value for x in current)):
        return "urgent"
    if any(x in value for x in QUOTED) or any(re.search(x, value) for x in DENIAL):
        return "uncertain" if any(x in value for x in UNCERTAIN) else "normal"
    if any(x in value for x in UNCERTAIN):
        return "uncertain"
    return "normal"
