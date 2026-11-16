"""Sem resultados inventados, sem afirmação jurídica da Groq."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from paths_validate import validate
from path_schema import SCHEMA
from intent_routing import allowed_categories
from privacy import minimal_context

GOOD = {"topic":"direitos", "category":"family", "result_kind":"map", "paths":[
    {"title":"Conhecer alternativas", "possibility":"Uma possibilidade é conhecer condições gerais antes de decidir.", "question":"Que informações jurídicas seriam relevantes?"},
    {"title":"Buscar orientação", "possibility":"Outra possibilidade é listar perguntas para uma orientação futura.", "question":"Onde é possível conhecer as condições?"}]}

class Agent(unittest.TestCase):
    def test_groq_schema_is_strict_friendly(self):
        self.assertFalse(SCHEMA["additionalProperties"])
        self.assertEqual(set(SCHEMA["required"]), set(SCHEMA["properties"]))
        self.assertFalse(SCHEMA["properties"]["paths"]["items"]["additionalProperties"])
        self.assertTrue(validate(GOOD, "direitos", {"family"}))

    def test_no_promises_or_unvalidated_categories(self):
        self.assertFalse(validate({**GOOD, "category":"protection"}, "direitos", {"family"}))
        bad = [{**p} for p in GOOD["paths"]]
        bad[0]["question"] = "Você com certeza vai ganhar?"
        self.assertFalse(validate({**GOOD, "paths":bad}, "direitos", {"family"}))
        self.assertFalse(validate({**GOOD, "paths":[]}, "direitos", {"family"}))

    def test_no_pressure_or_direct_contact(self):
        for phrase in ("Negocie diretamente com seu ex sobre a casa.",
                       "Venda a casa para conseguir sair.",
                       "Mude-se para um quarto e aguarde.",
                       "Avise seu parceiro sobre seus planos."):
            paths = [{**GOOD["paths"][0], "possibility": "Se quiser, " + phrase}, GOOD["paths"][1]]
            self.assertFalse(validate({**GOOD, "paths": paths}, "direitos", {"family"}), phrase)

    def test_safe_intent_routing(self):
        for phrase, expected in [("ele pode tomar meus filhos", "family"),
                                 ("ele pode tomar conta do meu dinheiro", "justice"),
                                 ("como fica minha casa se separar", "family"),
                                 ("ele controla meu salario", "justice")]:
            safe = minimal_context("direitos", phrase)
            self.assertEqual(allowed_categories(safe["concerns"]), {expected})
        mixed = minimal_context("direitos", "denunciar agressao e ele tirou meus filhos")
        self.assertFalse(allowed_categories(mixed["concerns"]))
