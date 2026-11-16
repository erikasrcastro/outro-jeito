import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from senado_live import ementa


class ExcerptTests(unittest.TestCase):
    def test_short_ementa_is_preserved(self):
        short = "Cria mecanismos de proteção e garantias legais."
        self.assertEqual(ementa({"Ementa": short}), short)

    def test_long_ementa_does_not_end_mid_word(self):
        long = "Cria mecanismos de proteção para situações legais. " + "Garantias previstas em lei " * 20
        snippet = ementa({"Ementa": long})
        self.assertLessEqual(len(snippet), 180)
        self.assertTrue(snippet.endswith("…"))
        self.assertIn(snippet[:-1], long)
