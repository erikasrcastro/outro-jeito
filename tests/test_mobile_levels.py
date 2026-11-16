from pathlib import Path
import unittest

WEB = Path(__file__).resolve().parents[1] / 'web'

class MobileLevelsTests(unittest.TestCase):
    def test_no_native_dropdown(self):
        html = (WEB / 'index.html').read_text()
        self.assertNotIn('<select', html)
        self.assertIn('name="difficulty" value="easy" checked', html)
        self.assertIn('name="difficulty" value="hard"', html)

    def test_accessible_fixed_controls(self):
        css = (WEB / 'styles.css').read_text()
        script = (WEB / 'game.js').read_text()
        self.assertIn('.levels { display: inline-flex; max-width: 100%', css)
        self.assertIn('.levels input:focus-visible + span', css)
        self.assertIn('levels.addEventListener("change", reset)', script)

if __name__ == '__main__':
    unittest.main()
