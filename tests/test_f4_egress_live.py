"""Valida payload do adaptador real antes de simular envio HTTP."""
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from egress import validate_egress
from groq_live import interpret
from privacy import minimal_context

class Reply:
    status=200
    async def text(self):
        return json.dumps({"choices":[{"message":{"content":json.dumps({
            "topic":"direitos", "category":"justice", "result_kind":"map", "paths":[
            {"title":"Conhecer alternativas", "possibility":"Uma possibilidade é conhecer opções de apoio jurídico.", "question":"Que informações oficiais podem ajudar?"},
            {"title":"Comparar cenários", "possibility":"Outra possibilidade é preparar dúvidas para orientação.", "question":"Quais condições precisam ser esclarecidas?"}]})}}]})

class Outbound(unittest.IsolatedAsyncioTestCase):
    async def test_real_adapter_body_is_allowlisted(self):
        calls=[]
        async def http(url, **kw):
            calls.append((validate_egress(url,**kw), json.loads(kw["body"])))
            return Reply()
        raw="ele pode tomar conta do meu dinheiro?"
        safe=minimal_context("direitos",raw)
        await interpret(safe,"KEY_FAKE",http)
        provider, body=calls[0]
        self.assertEqual(provider,"groq")
        self.assertEqual(json.loads(body["messages"][1]["content"]),safe)
        self.assertNotIn(raw,json.dumps(body))
        self.assertNotIn("Maria",json.dumps(body))
