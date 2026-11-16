"""Caminhos não validados jamais ganham fonte nem evidência falsa."""
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from flow_live import explore_live

GOOD = {"topic":"direitos", "category":"family", "result_kind":"map", "paths":[
    {"title":"Conhecer condições", "possibility":"Uma possibilidade é entender quais condições podem importar.", "question":"Que informações fazem falta?"},
    {"title":"Buscar orientação", "possibility":"Outra possibilidade é procurar uma fonte institucional.", "question":"Onde buscar orientação pública?"}]}

class Reply:
    def __init__(self, data): self.data, self.status = data, 200
    async def text(self): return json.dumps(self.data)

class Errors(unittest.IsolatedAsyncioTestCase):
    async def test_llm_unvalidated_never_calls_senado(self):
        called=[]
        async def http(url, **kw):
            called.append(url)
            return Reply({"choices":[{"message":{"content":json.dumps({**GOOD,"category":"health"})}}]})
        out=await explore_live({"topic":"direitos","context":"guarda"},"fake-key",http)
        self.assertEqual(out["status"],"json")
        self.assertEqual(out["evidence"],"UNVERIFIED")
        self.assertEqual(len(called),1)

    async def test_no_source_for_working_hypotheses(self):
        seen=[]
        async def http(url, **kw):
            seen.append(url)
            data={**GOOD,"category":"work"}
            return Reply({"choices":[{"message":{"content":json.dumps(data)}}]})
        out=await explore_live({"topic":"caminhos","context":"trabalho"},"fake-key",http)
        self.assertEqual(out["status"],"json")  # tema errado não é aceito
        self.assertEqual(len(seen),1)
