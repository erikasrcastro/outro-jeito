"""Intenções gerais reconhecidas localmente; nenhuma conclusão jurídica."""
import re
from safety import normalize

PATTERNS = {
    "reporting": (r"\b(denunci\w*|delegacia|boletim de ocorrencia)\b",
                  r"\b(agress\w*|violenc\w*|ameac\w*|abuso)\b"),
    "financial_control": (r"\b(dinheiro|salario|rendimentos|conta bancaria|financas|bens)\b",
                          r"\b(tomar|control\w*|reter|imped\w*|apropri\w*|administr\w*)\b"),
    "custody_concern": (r"\b(filh[oa]s?|crianc[as]+|guarda|custodia)\b",
                        r"\b(tomar|tomou|tirar|tirou|levar|levou|perder|afastar|ficar com)\b"),
    "property_split": (r"\b(casa|imovel|apartamento|moradia|partilha|bens)\b",
                       r"\b(separ\w*|divorci\w*|partilh\w*|terminar|rompimento)\b"),
}

def intents(text):
    plain = normalize(text)
    return {name for name, (subject, action) in PATTERNS.items()
            if re.search(subject, plain) and re.search(action, plain)}
