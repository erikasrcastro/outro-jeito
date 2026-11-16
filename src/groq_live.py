"""Uma chamada Groq gera caminhos sem receber narrativa original."""
import asyncio
import json
from path_schema import SCHEMA
from path_prompt import SYSTEM

URL = "https://api.groq.com/openai/v1/chat/completions"


async def interpret(safe, key, transport):
    body = {"model": "openai/gpt-oss-20b", "temperature": 0,
            "max_completion_tokens": 800, "reasoning_effort": "low",
            "messages": [{"role": "system", "content": SYSTEM},
                         {"role": "user", "content": json.dumps(safe, ensure_ascii=False)}],
            "response_format": {"type": "json_schema", "json_schema": {
                "name": "possible_futures", "strict": True, "schema": SCHEMA}}}
    response = await asyncio.wait_for(transport(URL, method="POST", redirect="manual",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        body=json.dumps(body, ensure_ascii=False)), timeout=25)
    if response.status != 200:
        raise ValueError("Groq indisponível")
    raw = await response.text()
    if len(raw) > 40_000:
        raise ValueError("Resposta excede tamanho seguro")
    data = json.loads(raw)
    try:
        result = json.loads(data["choices"][0]["message"]["content"])
    except (ValueError, TypeError, KeyError, IndexError):
        return {}
    return result
