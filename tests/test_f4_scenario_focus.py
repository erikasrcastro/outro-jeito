"""Regressão: geração trata futuros condicionais, não FAQ fixa."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from path_prompt import SYSTEM
from paths_validate import validate


class ScenarioFocus(unittest.TestCase):
    def test_prompt_distinguishes_scenarios_and_referrals(self):
        for term in ("FUTUROS POSSÍVEIS", "property_split", "partilha",
                     "uso/permanência", "HIPÓTESES", "não produzir"):
            self.assertIn(term, SYSTEM)

    def test_distinct_conditional_paths_validate(self):
        paths = [
            {"title":"Uso da moradia", "possibility":"Se o imóvel for alugado, o contrato pode mudar quais possibilidades precisam ser esclarecidas.", "question":"O vínculo com o imóvel é aluguel ou propriedade?"},
            {"title":"Titularidade e partilha", "possibility":"Caso o imóvel seja próprio, a forma de aquisição pode ser relevante para avaliar cenários de divisão.", "question":"A casa foi adquirida antes ou durante a relação?"},
            {"title":"Moradia alternativa", "possibility":"Dependendo da situação financeira, podem existir alternativas habitacionais a investigar.", "question":"Há alguma opção temporária de moradia que queira conhecer?"},
        ]
        data = {"topic":"direitos", "category":"family", "result_kind":"map", "paths":paths}
        self.assertTrue(validate(data, "direitos", {"family"}))
