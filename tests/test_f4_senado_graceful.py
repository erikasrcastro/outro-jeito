"""Uma falha da fonte não pode apagar hipóteses já validadas."""
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from flow_live import explore_live

PATHS = [
    {"title": "Entender as condições", "possibility": "Uma possibilidade é conhecer as informações necessárias antes de decidir.", "question": "Quais condições ainda precisam de confirmação?"},
    {"title": "Buscar orientação local", "possibility": "Outra possibilidade é buscar apoio jurídico de forma voluntária.", "question": "Qual serviço institucional seria apropriado?"},
]

class Reply:
    def __init__(self, value, status=200): self.value, self.status = value, status
    async def text(self): return json.dumps(self.value)

class SenateFailure(unittest.IsolatedAsyncioTestCase):
    async def check_failure(self, broken):
        calls = []
        async def http(url, **kwargs):
            calls.append(url)
            if "groq.com" in url:
                data = {"topic":"direitos", "category":"family", "result_kind":"map", "paths":PATHS}
                return Reply({"choices":[{"message":{"content":json.dumps(data)}}]})
            return Reply({}, 503) if broken == "http" else Reply({"Numero":10406,"Ano":2002})
        result = await explore_live({"topic":"direitos","context":"property_split"}, "fake-key", http)
        self.assertEqual(len(calls), 2)
        self.assertEqual((result["status"], result["evidence"]), ("futures", "UNVERIFIED"))
        self.assertIn(len(result["paths"]), (2, 3))
        self.assertTrue(all(p["evidence"] == "HYPOTHESIS" for p in result["paths"]))
        self.assertFalse(result["source_verified"])
        self.assertNotIn("Fonte legislativa localizada", result["message"])
        self.assertIn("Não consegui conferir a lei no Senado", result["message"])
        self.assertEqual(result["primary_action"]["id"], "open_official_source")

    async def test_503_keeps_validated_paths(self): await self.check_failure("http")
    async def test_incomplete_metadata_keeps_validated_paths(self): await self.check_failure("metadata")
