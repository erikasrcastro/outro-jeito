"""Texto simples sem perder limites de prova e segurança."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from path_prompt import SYSTEM
from property_paths import PATHS
from results_live import futures_response


class PlainLanguage(unittest.TestCase):
    def test_examples_and_conditional_paths(self):
        self.assertIn("Por exemplo:", SYSTEM)
        self.assertIn("8 anos", SYSTEM)
        self.assertEqual(len(PATHS), 3)
        for path in PATHS:
            self.assertIn("Por exemplo:", path["possibility"])
            self.assertTrue(path["possibility"].startswith(("Se", "Caso", "Dependendo")))
            self.assertLessEqual(len(path["possibility"]), 200)

    def test_verified_and_unverified_are_clear(self):
        extraction = {"category": "family", "paths": PATHS}
        source = {"reference": "Lei 10.406/2002", "url": "https://legis.senado.leg.br/"}
        result = futures_response(extraction, source, concerns={"property_split"})
        self.assertIn("não promessas", result["message"])
        self.assertIn("não quer dizer que vale", result["message"])
        self.assertEqual(result["evidence"], "CONDITIONAL")
        result = futures_response(extraction, source_failed=True, concerns={"property_split"})
        self.assertIn("Não consegui conferir a lei", result["message"])
        self.assertEqual(result["evidence"], "UNVERIFIED")
