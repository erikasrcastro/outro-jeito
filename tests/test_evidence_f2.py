import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from engine import explore
from evidence import valid_extraction, valid_source
from texts import MESSAGES, fallback
from mocks import groq, senado


class EvidenceF2(unittest.TestCase):
    def test_json_requires_exact_schema(self):
        self.assertTrue(valid_extraction(groq({"topic": "direitos"})))
        self.assertFalse(valid_extraction({"topic": "direitos", "category": "protection"}))
        self.assertFalse(valid_extraction({**groq({"topic": "direitos"}), "nome": "Pessoa"}))

    def test_simulated_senate_is_never_verified(self):
        result = explore({"topic": "direitos"}, groq, senado)
        self.assertEqual(result["status"], "preview")
        self.assertEqual(result["evidence"], "UNVERIFIED")
        self.assertFalse(valid_source({"simulated": True}))
        self.assertFalse(valid_source({"url": "https://legis.senado.leg.br.evil.com"}))

    def test_failures_have_actionable_next_step(self):
        for key in MESSAGES:
            with self.subTest(key=key):
                result = fallback(key)
                self.assertTrue(result["message"])
                self.assertTrue(result["primary_action"]["label"])
                self.assertTrue(result["secondary_action"]["id"])

    def test_api_errors_are_textual_not_fake(self):
        def broken(*args):
            raise TimeoutError("timeout")
        case = {"topic": "direitos", "context": "entender direitos"}
        self.assertEqual(explore(case, broken, senado)["status"], "groq")
        self.assertEqual(explore(case, groq, broken)["status"], "senado")
