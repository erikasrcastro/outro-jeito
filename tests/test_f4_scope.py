"""Nove domínios, consentimento e fonte na categoria legal."""
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from domains import DOMAINS, candidates
from flow_live import explore_live
from privacy import minimal_context

class Reply:
    status = 200
    def __init__(self, data): self.data = data
    async def text(self): return json.dumps(self.data)

class ScopeTests(unittest.IsolatedAsyncioTestCase):
    async def test_nine_domains_and_private_input(self):
        terms = ["protecao", "guarda", "trabalho", "assistencia", "moradia", "saude",
                 "acessibilidade", "crianca", "defensoria"]
        self.assertEqual(len(DOMAINS), 9)
        for term in terms:
            safe = minimal_context("direitos", f"Quero conhecer {term}")
            self.assertEqual(len(candidates(safe["concerns"])), 1)
            self.assertNotIn("Quero conhecer", str(safe))

    async def test_ambiguous_or_empty_stops_without_api(self):
        async def forbidden(*a, **kw): self.fail("API indevida")
        for text, status in [("guarda dos filhos após agressao", "clarify"),
                             ("uma questão desconhecida", "general")]:
            out = await explore_live({"topic":"direitos", "context":text}, "key", forbidden)
            self.assertEqual(out["status"], status)

    async def test_family_law_requires_real_normalized_source(self):
        visited = []
        async def http(url, **kw):
            visited.append(url)
            if "groq.com" in url:
                out = {"topic":"direitos", "category":"family", "result_kind":"map", "paths":[
                    {"title":"Guarda e convivência", "possibility":"Uma possibilidade é entender diferenças entre guarda e convivência.", "question":"Quais condições precisam ser esclarecidas?"},
                    {"title":"Apoio institucional", "possibility":"Outra possibilidade é procurar orientações sobre os requisitos.", "question":"Onde buscar orientação adequada?"}]}
                return Reply({"choices":[{"message":{"content":json.dumps(out)}}]})
            return Reply({"Norma":{"Numero":10406,"Ano":2002,
                "Ementa":"Institui o Código Civil, lei federal de caráter geral."}})
        result = await explore_live({"topic":"direitos", "context":"guarda"}, "key", http)
        self.assertEqual(result["evidence"], "CONDITIONAL")
        self.assertIn("10406/2002.json", visited[-1])
        self.assertEqual(len(visited), 2)
