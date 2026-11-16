import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from safety import urgency
from engine import explore


def forbidden(*args):
    raise AssertionError("API chamada indevidamente")


class SafetyF2(unittest.TestCase):
    def test_imminent_emergency_skips_both_apis(self):
        for text in ("socorro", "está me agredindo agora", "não consigo respirar", "não estou em perigo, mas ele vai me matar"):
            with self.subTest(text=text):
                result = explore({"topic": "direitos", "context": text}, forbidden, forbidden)
                self.assertEqual(result["status"], "urgent")
                self.assertEqual(result["primary_action"]["id"], "show_help")
                self.assertEqual(result["secondary_action"]["id"], "switch_game")

    def test_uncertain_not_declared_safe(self):
        self.assertEqual(urgency("tenho medo de mudar"), "uncertain")
        self.assertNotEqual(urgency("não estou em perigo agora"), "urgent")
        self.assertNotEqual(urgency("li uma notícia que dizia socorro"), "urgent")
        self.assertNotEqual(urgency("não está armado"), "urgent")
        self.assertNotEqual(urgency("não me trancou"), "urgent")

    def test_invalid_input_never_calls_api(self):
        for invalid in ([], {"topic": "foo"}, {"topic": "direitos", "idade": 20}):
            with self.subTest(invalid=invalid):
                self.assertIn(explore(invalid, forbidden, forbidden)["status"], ("invalid", "clarify"))
