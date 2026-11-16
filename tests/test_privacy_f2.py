import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from engine import explore
from privacy import has_identifiers, minimal_context


class PrivacyF2(unittest.TestCase):
    def test_personal_data_blocks_provider_calls(self):
        def forbidden(*args):
            raise AssertionError("PII foi transmitida")
        for p in ("Maria@example.com", "123.456.789-09", "Rua do Exemplo, 22"):
            with self.subTest(p=p):
                result = explore({"topic": "direitos", "context": p}, forbidden, forbidden)
                self.assertEqual(result["status"], "privacy")
                self.assertEqual(result["primary_action"]["id"], "edit_text")
                self.assertEqual(result["secondary_action"]["id"], "use_guided_options")

    def test_only_curated_tags_leave_preprocessor(self):
        captured = []
        def groq(safe):
            captured.append(str(safe))
            return {"topic": "direitos", "category": "protection", "result_kind": "map"}
        def senado(category):
            captured.append(str(category))
            return {"simulated": True}
        raw = "Alguém controla meus contatos e minha renda: CANARY_TESTE_99"
        result = explore({"topic": "direitos", "context": raw}, groq, senado)
        self.assertEqual(result["status"], "preview")
        self.assertNotIn("CANARY_TESTE_99", "".join(captured))
        self.assertNotIn("Alguém", "".join(captured))
        self.assertEqual(minimal_context("direitos", raw)["topic"], "direitos")
