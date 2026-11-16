import sys
import json
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from flow_live import explore_live
from senado_live import lookup


class BadReply:
    def __init__(self, body):
        self.body, self.status = body, 200
    async def text(self):
        return json.dumps(self.body)


class FailSafe(unittest.IsolatedAsyncioTestCase):
    async def test_senate_response_without_ementa_rejected(self):
        async def bad(_url, **_kw):
            return BadReply({"Numero": 11340, "Ano": 2006})
        with self.assertRaises(ValueError):
            await lookup("protection", bad)

    async def test_without_groq_key_no_outbound(self):
        async def forbidden(*a, **kw):
            raise AssertionError("Não deve acessar a rede")
        response = await explore_live({"topic": "direitos", "context": "proteção"}, None, forbidden)
        self.assertEqual(response["status"], "groq")
        self.assertEqual(response["primary_action"]["id"], "show_general")
        self.assertFalse(response["simulated"])
