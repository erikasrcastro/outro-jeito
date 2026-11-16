"""A LLM não confirma leis nem define o estado da evidência."""
from urllib.parse import urlparse
from domains import DOMAINS

TOPICS = {"direitos", "apoio", "caminhos"}
KINDS = {"map", "clarify", "abstain"}
CATEGORIES = {*DOMAINS, "rights_information", "none"}


def valid_extraction(data):
    return (isinstance(data, dict) and set(data) == {"topic", "category", "result_kind"}
            and data.get("topic") in TOPICS and data.get("category") in CATEGORIES
            and data.get("result_kind") in KINDS)


def valid_source(data):
    if not isinstance(data, dict) or data.get("simulated") is True:
        return False
    address = data.get("url")
    if not isinstance(address, str):
        return False
    parsed = urlparse(address)
    return (parsed.scheme == "https" and parsed.hostname in {"legis.senado.leg.br", "legis.senado.gov.br"}
            and all(isinstance(data.get(key), str) and data[key].strip()
                    for key in ("reference", "checked_at", "title")))
