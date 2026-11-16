"""Perguntas não são FAQ: Groq deve criar opções, respeitando categoria."""
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from flow_live import explore_live

SAMPLES = [("onde posso denunciar agressão?", "protection"),
           ("ele pode tomar conta do meu dinheiro?", "justice"),
           ("ele pode tomar meus filhos de mim?", "family"),
           ("como fica minha casa se eu me separar?", "family")]

class Intents(unittest.IsolatedAsyncioTestCase):
    async def test_four_intents_use_dynamic_groq_and_only_needed_sources(self):
        for text, category in SAMPLES:
            seen = []
            async def http(url, **kw):
                seen.append((url, kw))
                if "groq.com" in url:
                    result = {"topic":"direitos", "category":category, "result_kind":"map", "paths":[
                        {"title":"Primeiro caminho", "possibility":"Uma possibilidade é conhecer informações oficiais aplicáveis.", "question":"Que informações podem ajudar a entender as alternativas?"},
                        {"title":"Segundo caminho", "possibility":"Outra possibilidade é entender opções de apoio institucional.", "question":"Onde buscar uma orientação para o próximo passo?"}]}
                    return Reply({"choices":[{"message":{"content":json.dumps(result)}}]})
                num, year = (11340,2006) if category == "protection" else (10406,2002)
                return Reply({"Norma":{"Numero":num,"Ano":year,
                    "Ementa":"Institui regras sobre direitos e proteção conforme a legislação federal."}})
            out = await explore_live({"topic":"direitos", "context":text}, "key", http)
            self.assertEqual(out["status"], "futures", text)
            self.assertIn(len(out["paths"]), (2, 3))
            self.assertEqual(len(seen), 1 if category == "justice" else 2)
            self.assertNotIn(text, str(seen))

class Reply:
    status = 200
    def __init__(self, data): self.data = data
    async def text(self): return json.dumps(self.data)
