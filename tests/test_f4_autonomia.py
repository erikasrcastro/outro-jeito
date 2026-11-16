"""Regressão sintética: proteção, autonomia e falha da fonte."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from path_prompt import SYSTEM
from results_live import futures_response
from property_paths import PATHS

LLM = {"category": "family", "paths": [
    {"title": "Negociar a casa com o parceiro", "possibility": "Caso queira, acerte as contas com ele.", "question": "Vai negociar?"},
    {"title": "Vender o imóvel", "possibility": "Se separar, venda a casa.", "question": "Vai vender?"}]}

class Autonomia(unittest.TestCase):
    def test_guardrail_replaces_risky_llm_suggestions(self):
        out = futures_response(LLM, concerns={"property_split"})
        joined = " ".join(p["title"] + " " + p["possibility"] for p in out["paths"]).lower()
        self.assertEqual(len(out["paths"]), 3)
        self.assertNotIn("negociar a casa", joined)
        self.assertNotIn("vender o imóvel", joined)
        self.assertIn("proteção", joined)
        self.assertIn("apoio", SYSTEM)
        self.assertIn("partilha", joined)
        self.assertIn("180", joined)
        self.assertIn("não precisa decidir", out["message"])

    def test_senado_failure_keeps_choices_without_false_verification(self):
        out = futures_response(LLM, source_failed=True, concerns={"property_split"})
        self.assertFalse(out["source_verified"])
        self.assertEqual(out["evidence"], "UNVERIFIED")
        self.assertTrue(all(p["evidence"] == "HYPOTHESIS" for p in out["paths"]))
        self.assertEqual(out["source"]["source_kind"], "official_guide")
        self.assertIn("gov.br/mulheres", out["source"]["url"])

    def test_other_topics_preserve_dynamic_paths(self):
        out = futures_response(LLM, concerns={"custody_concern"})
        self.assertEqual(out["paths"][0]["title"], LLM["paths"][0]["title"])
        self.assertEqual(out["source"]["source_kind"], "official_guide")

    def test_protected_paths_are_short_and_conditional(self):
        self.assertEqual(len(PATHS), 3)
        for item in PATHS:
            self.assertLessEqual(len(item["possibility"]), 200)
            self.assertTrue(item["possibility"].startswith(("Se", "Caso", "Dependendo")))
            self.assertTrue(item["question"].endswith("?"))
