import sys
import json
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from flow_live import explore_live

PATHS = [{"title": "Conhecer orientações", "possibility": "Uma possibilidade é consultar referências públicas antes de decidir.", "question": "Onde existem referências oficiais sobre essa situação?"},
         {"title": "Explorar alternativas", "possibility": "Outra possibilidade é organizar dúvidas e fontes de apoio.", "question": "Quais informações ainda seriam úteis conhecer?"}]

class Reply:
    def __init__(self, val, status=200): self.val, self.status = val, status
    async def text(self): return json.dumps(self.val)

class Flow(unittest.IsolatedAsyncioTestCase):
    async def test_no_external_call_on_urgent_or_pii(self):
        async def forbidden(*a, **kw): self.fail("API não deve ser chamada")
        for phrase, expected in [("socorro", "urgent"), ("meu nome é Maria", "privacy")]:
            out = await explore_live({"topic": "direitos", "context": phrase}, "key", forbidden)
            self.assertEqual(out["status"], expected)

    async def test_fiap_t1_pipeline_t2_and_t3(self):
        seen = []
        async def http(url, **kw):
            seen.append((url, kw))
            if "groq.com" in url:
                data = {"topic": "direitos", "category": "protection", "result_kind": "map", "paths": PATHS}
                return Reply({"choices": [{"message": {"content": json.dumps(data)}}]})
            return Reply({"Norma": {"Numero": 11340, "Ano": 2006,
                "Ementa": "Cria mecanismos para coibir a violência doméstica e familiar contra a mulher."}})
        case = {"topic": "direitos", "context": "quero entender proteção e contatos"}
        out = await explore_live(case, "key", http)
        self.assertEqual(out["status"], "futures")
        self.assertEqual(out["evidence"], "CONDITIONAL")
        self.assertEqual(len(out["paths"]), 2)
        self.assertEqual(len(seen), 2)
        self.assertNotIn(case["context"], str(seen))
        seen.clear()
        self.assertEqual((await explore_live({"topic": "invalido"}, "key", http))["status"], "clarify")
        self.assertEqual(seen, [])
        async def broken(url, **kw):
            resp = await http(url, **kw)
            return Reply({}, 503) if "senado" in url else resp
        out = await explore_live(case, "key", broken)
        self.assertEqual((out["status"], out["evidence"]), ("futures", "UNVERIFIED"))
        self.assertEqual(len(out["paths"]), 2)
        self.assertIn("Não consegui conferir a lei no Senado", out["message"])
