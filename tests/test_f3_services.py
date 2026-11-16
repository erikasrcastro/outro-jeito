import sys
import json
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from groq_live import interpret, URL
from senado_live import lookup, API

class Reply:
    def __init__(self, value, status=200): self.value, self.status = value, status
    async def text(self): return json.dumps(self.value)

class Services(unittest.IsolatedAsyncioTestCase):
    async def test_groq_payload_is_minimized_and_strict(self):
        seen = []
        async def http(url, **kw):
            seen.append((url, kw))
            content = {"topic":"direitos", "category":"protection", "result_kind":"map", "paths":[
                {"title":"Conhecer opções", "possibility":"Uma possibilidade é comparar informações oficiais sem pressa.", "question":"Que tipo de informação oficial pode ajudar?"},
                {"title":"Consultar uma fonte", "possibility":"Outra possibilidade é buscar orientação institucional confiável.", "question":"Onde buscar orientação sobre este assunto?"}]}
            return Reply({"choices":[{"message":{"content":json.dumps(content)}}]})
        safe = {"topic":"direitos", "concerns":["contatos"], "jurisdiction":"BR"}
        out = await interpret(safe, "SYNTHETIC_KEY", http)
        self.assertEqual(out["category"], "protection")
        self.assertEqual(seen[0][0], URL)
        sent = json.loads(seen[0][1]["body"])
        self.assertTrue(sent["response_format"]["json_schema"]["strict"])
        self.assertIn("paths", sent["response_format"]["json_schema"]["schema"]["properties"])
        self.assertNotIn("NOME_TESTE_K9", seen[0][1]["body"])

    async def test_senado_uses_fixed_id_and_real_ementa(self):
        seen = []
        async def http(url, **kw):
            seen.append(url)
            return Reply({"Norma":{"Numero":11340,"Ano":2006,
                "Ementa":"Cria mecanismos para coibir a violência doméstica e familiar contra a mulher."}})
        out = await lookup("protection", http)
        self.assertEqual(seen, [API])
        self.assertIn("violência doméstica", out["title"])
        self.assertFalse(out["simulated"])
