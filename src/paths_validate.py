"""Validação semântica conservadora após JSON estrito."""
import re
from path_schema import safe_paths
from safety import normalize

BANNED = (
    r"\b(garantid[oa]|certeza|com certeza|sempre|nunca perde|vai ganhar)\b",
    r"\b(confronte|ameace|fuja escondid|minta|hackeie|fraude)\b",
    r"\b(denuncie agora|separe-se agora|abandone seus filhos)\b",
    r"\b(negocie|converse|combine|acorde)\b.{0,60}\b(com|diretamente)\b.{0,25}\b(agressor|ele|ex|parceiro|marido)\b",
    r"\b(venda|alugue)\b.{0,18}\b(casa|imovel|moradia)\b",
    r"\b(saia|mude.se)\b.{0,25}\b(casa|quarto)\b",
    r"\b(avise|conte)\b.{0,30}\b(agressor|parceiro|marido|ex)\b",
)


def validate(data, topic, allowed):
    if not safe_paths(data) or data.get("topic") != topic:
        return False
    if data.get("category") not in allowed or data.get("result_kind") != "map":
        return False
    for path in data["paths"]:
        text = normalize(path["title"] + " " + path["possibility"] + " " + path["question"])
        if any(re.search(rule, text) for rule in BANNED):
            return False
    return True
