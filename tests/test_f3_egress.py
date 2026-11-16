import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from egress import validate_egress, GROQ, SENADO


def groq(safe):
    return {"method": "POST", "redirect": "manual",
            "headers": {"Authorization": "Bearer CHAVE_FICTICIA", "Content-Type": "application/json"},
            "body": json.dumps({"messages": [{"role": "system", "content": "Classifique"},
                {"role": "user", "content": json.dumps(safe)}]})}


class EgressTests(unittest.TestCase):
    def test_groq_allows_only_minimized_contract(self):
        safe = {"topic": "direitos", "concerns": ["contatos"], "jurisdiction": "BR"}
        self.assertEqual(validate_egress(GROQ, **groq(safe)), "groq")

    def test_canary_and_extra_fields_are_blocked(self):
        for value in ["NOME_TESTE_K9", "Rua Exemplo", "meu nome é Maria"]:
            safe = {"topic": "direitos", "concerns": [value], "jurisdiction": "BR"}
            with self.assertRaises(ValueError):
                validate_egress(GROQ, **groq(safe))
        safe = {"topic": "direitos", "concerns": [], "jurisdiction": "BR", "cpf": "00000000000"}
        with self.assertRaises(ValueError):
            validate_egress(GROQ, **groq(safe))

    def test_only_fixed_senado_get_is_allowed(self):
        opts = {"method": "GET", "redirect": "manual", "headers": {"Accept": "application/json"}}
        self.assertEqual(validate_egress(SENADO, **opts), "senado")
        for url in ["https://evil.invalid", SENADO + "?context=nome"]:
            with self.assertRaises(ValueError):
                validate_egress(url, **opts)
        with self.assertRaises(ValueError):
            validate_egress(SENADO, **{**opts, "headers": {"Authorization": "Bearer CHAVE_FICTICIA"}})
