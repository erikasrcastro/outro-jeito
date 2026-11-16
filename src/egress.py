"""Guardrail de saída: valida o último payload antes do HTTP real."""
import json
from privacy import TAGS, TOPICS
from groq_live import URL as GROQ
from senado_live import API as SENADO, URLS

SAFE_CONCERNS = set(TAGS.values())


def validate_egress(url, **options):
    method, headers = options.get("method"), options.get("headers") or {}
    if url == GROQ:
        if method != "POST" or options.get("redirect") != "manual":
            raise ValueError("Transporte Groq não permitido")
        if set(headers) != {"Authorization", "Content-Type"} or not headers["Authorization"].startswith("Bearer "):
            raise ValueError("Cabeçalhos Groq inválidos")
        if headers["Content-Type"] != "application/json":
            raise ValueError("Tipo Groq inválido")
        try:
            body = json.loads(options["body"])
            messages = body["messages"]
            safe = json.loads(messages[1]["content"])
        except (KeyError, ValueError, TypeError, IndexError) as error:
            raise ValueError("Payload Groq inválido") from error
        if len(messages) != 2 or [m.get("role") for m in messages] != ["system", "user"]:
            raise ValueError("Mensagens Groq inválidas")
        if not isinstance(safe, dict) or set(safe) != {"topic", "concerns", "jurisdiction"}:
            raise ValueError("Campos não permitidos")
        concerns = safe["concerns"]
        if safe["topic"] not in TOPICS or safe["jurisdiction"] != "BR":
            raise ValueError("Contexto fora do contrato")
        if type(concerns) is not list or len(concerns) > 5 or any(type(c) is not str or c not in SAFE_CONCERNS for c in concerns):
            raise ValueError("Etiquetas fora do contrato")
        return "groq"
    if url in URLS.values() and method == "GET" and options.get("redirect") == "manual":
        if headers == {"Accept": "application/json"} and not options.get("body"):
            return "senado"
    raise ValueError("Destino ou requisição não permitidos")


def audit_egress(provider, enabled):
    if enabled:
        print(f"EGRESS_AUDIT provider={provider} payload=allowlisted")
