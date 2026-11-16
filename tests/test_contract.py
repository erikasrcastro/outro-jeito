from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def test_html_has_next_steps(self):
        html = (ROOT / "web/index.html").read_text()
        for expected in ('id="switch"', 'id="help"', 'id="back"', '<noscript>', 'id="game"'):
            self.assertIn(expected, html)

    def test_no_remote_frontend_dependencies(self):
        html = (ROOT / "web/index.html").read_text()
        self.assertNotIn("https://", html)
        self.assertNotIn("localStorage", html)

    def test_phase_three_worker_uses_real_adapters(self):
        code = (ROOT / "src/main.py").read_text()
        self.assertIn('from flow_live import explore_live', code)
        self.assertIn('from workers import WorkerEntrypoint, Response, fetch', code)
        self.assertNotIn('from mocks import', code)
        self.assertIn('GROQ_API_KEY', code)
        self.assertNotIn('print(', code)
        self.assertIn('"apis_connected": False', code)

if __name__ == "__main__":
    unittest.main()
