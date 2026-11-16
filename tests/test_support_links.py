import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from local_guides import GUIDES
from scope import GUIDES as LEGACY

class SupportLinks(unittest.TestCase):
    def test_family_link_is_a_state_directory(self):
        target = "https://www.cnj.jus.br/poder-judiciario/defensoria-publica/"
        self.assertEqual(GUIDES["family"][1], target)
        self.assertEqual(GUIDES["justice"][1], target)
        self.assertEqual(LEGACY["custody"], target)
        self.assertIn("estado", GUIDES["family"][2])

    def test_no_generic_ministerio_publico_article(self):
        self.assertTrue(all("defensoria-publica-e-ministerio" not in
                            val[1] for val in GUIDES.values()))

if __name__ == "__main__":
    unittest.main()
