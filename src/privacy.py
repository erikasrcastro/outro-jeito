"""PII é bloqueada; o MVP transmite só etiquetas autorizadas."""
import re
from safety import normalize
from meaning import intents

PII = (
    r"\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b",
    r"\b\d{3}[. ]?\d{3}[. ]?\d{3}[-. ]?\d{2}\b",
    r"\b\d{5}-?\d{3}\b",
    r"\b(?:\+?55\s?)?(?:\(?\d{2}\)?\s?)?9\d{4}[- ]?\d{4}\b",
    r"\b(?:rua|avenida|travessa|alameda|cep|meu nome e|me chamo|se chama)\b",
)
TAGS = {word: word for word in (
    "contatos controle moradia renda protecao direitos guarda custodia trabalho emprego "
    "agressao violencia ameaca convivencia pensao divorcio separacao alimentos visitas "
    "desemprego salario qualificacao curso cras creas cadunico beneficio assistencia bpc "
    "aluguel habitacao abrigo despejo saude sus medico psicologo terapia hospital "
    "acessibilidade deficiencia autismo discriminacao crianca adolescente menor escola "
    "defensoria advogado justica processo documento juridica"
).split()}
TAGS.update({"controle": "autonomia", "custodia": "guarda"})
TAGS.update({code: code for code in ("reporting", "financial_control", "custody_concern", "property_split")})
TOPICS = {"direitos", "apoio", "caminhos"}

def has_identifiers(text):
    simple = normalize(text)
    return any(re.search(rule, simple, re.I) for rule in PII)

def minimal_context(topic, text):
    simple = normalize(text)
    found = sorted({value for word, value in TAGS.items() if re.search(r"\b" + word + r"\b", simple)} | intents(simple))
    return {"topic": topic, "concerns": found[:5], "jurisdiction": "BR"}
