"""O modelo sugere perguntas; não verifica fatos, direitos ou fontes."""
import re
from domains import DOMAINS

ITEM = {"type": "object", "additionalProperties": False,
        "properties": {"title": {"type": "string"}, "possibility": {"type": "string"},
                       "question": {"type": "string"}},
        "required": ["title", "possibility", "question"]}
SCHEMA = {"type": "object", "additionalProperties": False,
          "properties": {
              "topic": {"type": "string", "enum": ["direitos", "apoio", "caminhos"]},
              "category": {"type": "string", "enum": [*DOMAINS, "none"]},
              "result_kind": {"type": "string", "enum": ["map", "clarify", "abstain"]},
              "paths": {"type": "array", "items": ITEM}},
          "required": ["topic", "category", "result_kind", "paths"]}


def safe_paths(data):
    if not isinstance(data, dict) or set(data) != set(SCHEMA["properties"]):
        return False
    paths = data.get("paths")
    if not isinstance(paths, list) or not 2 <= len(paths) <= 3:
        return False
    for item in paths:
        if not isinstance(item, dict) or set(item) != {"title", "possibility", "question"}:
            return False
        title, question, possibility = item["title"], item["question"], item["possibility"]
        if any(not isinstance(value, str) for value in (title, possibility, question)):
            return False
        if not 5 <= len(title) <= 65 or not 25 <= len(possibility) <= 200 or not 12 <= len(question) <= 180:
            return False
        if not question.endswith("?") or re.search(r"https?://|@|\d{5,}", title + possibility + question):
            return False
    return len({x["title"].casefold() for x in paths}) == len(paths)
