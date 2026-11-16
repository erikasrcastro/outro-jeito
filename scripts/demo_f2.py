"""Prévia F2: dados fictícios, sem APIs externas."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from engine import explore
from mocks import groq, senado

cases = {
    "URGENCIA": {"topic": "direitos", "context": "está me agredindo agora"},
    "PRIVACIDADE": {"topic": "direitos", "context": "Rua Exemplo, 22"},
    "MOCK DO SENADO": {"topic": "direitos", "context": "entender meus direitos"},
    "ENTRADA INCOMPLETA": {"context": ""},
}
for name, payload in cases.items():
    result = explore(payload, groq, senado)
    print(f"\n--- {name} ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))
